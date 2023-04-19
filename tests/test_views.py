from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from electron.models import (
    Category,
    Product,
    Order,
    OrderItem,
    Cart,
    CartItem,
)


class PublicViewLoginRequiredTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user",
            password="password"
        )
        cls.category = Category.objects.create(
            name="category",
            image="image"
        )
        cls.product = Product.objects.create(
            name="product",
            description="description",
            price=100,
            cover_image="cover_image",
            category=cls.category
        )
        cls.category = Category.objects.create(
            name="category",
            image="image"
        )
        cls.product = Product.objects.create(
            name="product",
            description="description",
            price=100,
            cover_image="cover_image",
            category=cls.category
        )
        cls.order = Order.objects.create(
            user=cls.user
        )
        cls.order_item = OrderItem.objects.create(
            product=cls.product,
            order=cls.order,
            amount=1
        )
        cls.cart = Cart.objects.create(
            user=cls.user
        )
        cls.cart_item = CartItem.objects.create(
            product=cls.product,
            cart=cls.cart,
            amount=1
        )

    def test_category_list(self):
        response = self.client.get(reverse("electron:category-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "electron/category_list.html")

    def test_product_list(self):
        response = self.client.get(
            reverse("electron:product-list", args=[self.category.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "electron/product_list.html")

    def test_product_details(self):
        response = self.client.get(
            reverse("electron:product-detail", args=[self.product.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "electron/product_detail.html")

    def test_cart(self):
        response = self.client.get(reverse("electron:cart"))

        self.assertEqual(response.status_code, 302)

    def test_delete_from_cart(self):
        response = self.client.get(
            reverse("electron:delete-from-cart", args=[self.cart_item.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_order(self):
        response = self.client.get(reverse("electron:orders"))

        self.assertEqual(response.status_code, 302)

    def test_search(self):
        response = self.client.get(reverse("electron:search"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "electron/search.html")
