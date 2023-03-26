from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="product"
    )

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(
        Product,
        related_name="carts",
        through="CartItem"
    )


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    product = models.ManyToManyField(
        Product,
        related_name="orders",
        through="OrderItem"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    image = models.ImageField(upload_to="images/products/")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_item"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_item"
    )
    amount = models.IntegerField(default=0)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_item"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_item"
    )
    amount = models.IntegerField()
