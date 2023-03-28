from django.db.models import Sum, F, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem
)
from .forms import AddToCartForm, ProductSearchForm


class CategoryList(generic.ListView):
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        categories = context["category_list"]
        grouped_categories = [
            categories[i:i + 3]
            for i in range(0, len(categories), 3)
        ]
        context["grouped_categories"] = grouped_categories
        context["items_in_cart"] = get_count_items(self.request.user.id)
        context["search_form"] = ProductSearchForm()

        return context


class ProductList(generic.ListView):
    model = Product
    paginate_by = 8

    def get_queryset(self):
        queryset = Product.objects.filter(
            category__pk=self.kwargs["pk"]
        )
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(
                Q(name__icontains=name) |
                Q(description__icontains=name)
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["items_in_cart"] = get_count_items(self.request.user.id)

        context["category_name"] = Category.objects.get(
            pk=self.kwargs["pk"]).name

        context["category_id"] = self.kwargs["pk"]

        name = self.request.GET.get("name", "")
        context["search_form"] = ProductSearchForm(
            initial={"name": name}
        )

        return context


class ProductDetail(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddToCartForm
        context["items_in_cart"] = get_count_items(self.request.user.id)

        return context

    def post(self, request, pk=None):
        if request.user.is_authenticated:
            url = reverse_lazy("electron:product-detail", kwargs={"pk": pk})
            form = AddToCartForm(request.POST)
            user_id = request.user.id
            if form.is_valid() and pk:
                cart = Cart.objects.get_or_create(user_id=user_id)
                amount = form.cleaned_data["amount"]
                try:
                    cart_item = CartItem.objects.get(
                        cart=cart[0],
                        product_id=pk
                    )
                    cart_item.amount += int(amount)
                    cart_item.save()
                except ObjectDoesNotExist:
                    CartItem.objects.create(
                        cart=cart[0],
                        product_id=pk,
                        amount=amount
                    )

            return redirect(url)
        return redirect("login")


@login_required
def cart_view(request):
    if request.method == "GET":
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            cart = Cart.objects.create(user_id=request.user.id)

        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.select_related("product")

        sum_cart = (
            CartItem.objects.filter(cart=cart)
            .annotate(item_price=Sum(F('amount') * F('product__price')))
            .aggregate(total_price=Sum('item_price'))['total_price']
        )
        items_in_cart = get_count_items(request.user.id)
        context = {
            "cart_items": cart_items,
            "sum_cart": sum_cart,
            "items_in_cart": items_in_cart
        }

        return render(request, "electron/cart.html", context)

    elif request.method == "POST":
        cart_items = CartItem.objects.filter(
            cart=Cart.objects.get(user_id=request.user.id)
        ).select_related("product")
        if cart_items:
            order = Order.objects.create(user_id=request.user.id)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item.product_id,
                    amount=item.amount
                )
            cart_items.delete()
        return redirect("electron:cart")


class OrderList(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
                'order_item', 'order_item__product'
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items_in_cart"] = get_count_items(self.request.user.id)

        return context


class SearchProduct(generic.ListView):
    model = Product
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProductSearchForm(
            initial={"name": name}
        )
        context["items_in_cart"] = get_count_items(self.request.user.id)

        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return super().get_queryset().filter(
                Q(name__icontains=name) |
                Q(description__icontains=name)
            )
        return super().get_queryset()


@login_required
def delete_from_cart_view(request, pk):
    if request.method == 'POST':
        CartItem.delete_item_from_cart(request.user.id, pk)
    return redirect("electron:cart")


def get_count_items(user_id: int = None) -> int:
    items_in_cart = 0
    if user_id:
        items_in_cart = CartItem.count_items_in_cart(user_id)

    return items_in_cart
