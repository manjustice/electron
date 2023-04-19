from django.contrib.auth import get_user_model
from django.test import TestCase

from electron.models import Category, Product, Order, CartItem, OrderItem, Cart


class ModelsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test",
            password="test",
            email="test",
            first_name="test",
            last_name="test",
            phone_number="+30000000000",
        )
        self.category = Category.objects.create(
            name="test",
            image="image"
        )
        self.product_one = Product.objects.create(
            name="test",
            description="test",
            price=100,
            cover_image="cover_image",
            category=self.category
        )
        self.product_two = Product.objects.create(
            name="test",
            description="test",
            price=200,
            cover_image="cover_image",
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,

        )

    def test_category_str(self):
        category = Category.objects.create(
            name="test",
            image="image"
        )

        self.assertEqual(
            str(category),
            f"{category.name}"
        )

    def test_product_str(self):
        self.assertEqual(
            str(self.product_one),
            f"{self.product_one.name}"
        )

    def test_order_total_sum(self):
        order = Order.objects.create(
            user=self.user
        )

        OrderItem.objects.create(
            order=order,
            product=self.product_one,
            amount=1
        )
        OrderItem.objects.create(
            order=order,
            product=self.product_two,
            amount=2
        )

        self.assertEqual(int(order.total_sum()), 500)

    def test_items_in_cart_and_delete_item(self):
        cart = Cart.objects.create(
            user_id=self.user.id
        )

        CartItem.objects.create(
            cart=cart,
            product=self.product_one,
            amount=1
        )
        CartItem.objects.create(
            cart=cart,
            product=self.product_two,
            amount=2
        )

        self.assertEqual(CartItem.count_items_in_cart(user_id=self.user.id), 2)
        CartItem.delete_item_from_cart(user_id=self.user.id, product_id=self.product_one.id)
        self.assertEqual(CartItem.count_items_in_cart(user_id=self.user.id), 1)
