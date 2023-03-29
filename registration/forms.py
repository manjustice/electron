from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import TextInput, PasswordInput


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "E-mail"})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Phone number"})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Password"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password confirmation",
            }
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "phone_number",
            "password1",
            "password2"
        ]


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={
            "class": "validate",
            "placeholder": "username"}
        )
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={"placeholder": "Password"})
    )
