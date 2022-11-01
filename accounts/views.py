from .forms import AccountsForm, LoginForm
from django.views.generic import CreateView
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = AccountsForm
    model = User
    success_url = reverse_lazy("tweets:home")


class LoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class LogoutView(LogoutView):
    pass
