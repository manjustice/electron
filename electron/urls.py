from django.urls import path

from .views import (
    CategoryList,
    ProductList,
    ProductDetail,
    cart_view,
    OrderList
)


urlpatterns = [
    path("", CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>", ProductList.as_view(), name="product-list"),
    path("product/<int:pk>", ProductDetail.as_view(), name="product-detail"),
    path("cart/", cart_view, name="cart"),
    path("orders/", OrderList.as_view(), name="orders")
]

app_name = "electron"
