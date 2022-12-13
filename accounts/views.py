from django.shortcuts import redirect
from .forms import AccountsForm, FollowForm, LoginForm
from django.views.generic import CreateView, RedirectView
from .models import User, Follow, Friendship
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch


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


class FollowView(LoginRequiredMixin, RedirectView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        request = Friendship.objects.create(
            follower=self.request.user, followee=self.kwargs["username"]
        )
        return self.get(request, *args, **kwargs)
