from django.forms import ModelForm, CharField, TextInput
from django.core.exceptions import ValidationError

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
                "placeholder": "Enter a number"
            }
        ))

    class Meta:
        model = CartItem
        fields = ["amount"]

    def clean_license_number(self):
        number = self.cleaned_data["license_number"]
        if number < 1:
            raise ValidationError("License number should consist of 8 characters")