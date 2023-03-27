from django.urls import path

from .views import (
    CategoryList,
    ProductList,
    ProductDetail,
    cart_view,
    delete_from_cart_view,
    OrderList,
    SearchProduct
)


urlpatterns = [
    path("", CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>", ProductList.as_view(), name="product-list"),
    path("product/<int:pk>", ProductDetail.as_view(), name="product-detail"),
    path("cart/", cart_view, name="cart"),
    path("cart/<int:pk>/delete", delete_from_cart_view, name="delete-from-cart"),
    path("orders/", OrderList.as_view(), name="orders"),
    path("search/", SearchProduct.as_view(), name="search"),
]

app_name = "electron"
