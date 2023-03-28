from django.forms import ModelForm, CharField, TextInput
from django.core.exceptions import ValidationError
from django import forms

from .models import CartItem


class AddToCartForm(ModelForm):
    amount = CharField(
        required=True,
        widget=TextInput(
            attrs={
                "type": "number",
                'autocomplete': 'off',
                'pattern': '[0-9]+',
                'title': 'Enter numbers Only ',
                "placeholder": "Enter a number",
                "min": 0,
            }
        ))

    class Meta:
        model = CartItem
        fields = ["amount"]

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if int(amount) < 1:
            raise ValidationError("Amount must be 1 or greater")
        return amount


class ProductSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search product by name",
                                      "class": "form-control"})
    )
