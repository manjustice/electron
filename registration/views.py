from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views

from .forms import RegisterForm


class RegistrationView(generic.CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('electron:category-list')
        return super().dispatch(request, *args, **kwargs)


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('electron:category-list')
    return auth_views.LoginView.as_view()
