from .forms import AccountsForm, LoginForm
from django.views.generic import CreateView
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = AccountsForm
    model = User
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_pw)
        login(self.request, user)
        return response


class LoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class LogoutView(LogoutView):
    pass
