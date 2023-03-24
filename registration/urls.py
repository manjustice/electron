from django.urls import path

from .views import RegistrationView, custom_login
from .forms import CustomAuthForm


urlpatterns = [
    path("register/", RegistrationView.as_view(), name="registration"),
    path(
        "login/",
        custom_login,
        name="login",
    )
]
