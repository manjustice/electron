from django.test import TestCase

from electron.forms import AddToCartForm


class FormsTest(TestCase):
    def test_add_to_cart_product_if_more_than_one(self):
        form_data = {"amount": 10}

        form = AddToCartForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data, form_data)

    def test_add_to_cart_product_when_negative_number(self):
        form_data = {"amount": -10}

        form = AddToCartForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse(form.cleaned_data, form_data)
