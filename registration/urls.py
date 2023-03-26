from django.urls import path

from .views import RegistrationView, custom_login, custom_logout


urlpatterns = [
    path("register/", RegistrationView.as_view(), name="registration"),
    path("login/", custom_login, name="login",),
    path("logout/", custom_logout, name="logout")
]
