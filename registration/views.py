from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from .forms import RegisterForm


class RegistrationView(generic.CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("electron:category-list")
