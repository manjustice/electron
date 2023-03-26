from django.db.models import Sum, F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem
)
from .forms import AddToCartForm


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

        return context


class ProductList(generic.ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset().filter(category_id=self.kwargs.get("pk"))

        return queryset


class ProductDetail(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddToCartForm

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

            return HttpResponseRedirect(url)
        return redirect("login")


def cart_view(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            cart = Cart.objects.create(user_id=request.user.id)

        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.select_related("product")

        sum_cart = (
            CartItem.objects.filter(cart=cart).select_related("product")
            .annotate(item_price=Sum(F('amount') * F('product__price')))
            .aggregate(total_price=Sum('item_price'))['total_price']
        )

        context = {"cart_items": cart_items, "sum_cart": sum_cart}

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


class OrderList(generic.ListView):
    model = Order
    paginate_by = 5
