from django.urls import path

from .views import CategoryList, ProductList, ProductDetail


urlpatterns = [
    path("", CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>", ProductList.as_view(), name="product-list"),
    path("product/<int:pk>", ProductDetail.as_view(), name="product-detail")
]

app_name = "electron"
