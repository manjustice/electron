from django.views import generic

from .models import Category, Product


class CategoryList(generic.ListView):
    model = Category


class ProductList(generic.ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset().filter(category_id=self.kwargs.get("pk"))

        return queryset


class ProductDetail(generic.DetailView):
    model = Product
