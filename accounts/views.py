from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .forms import AccountsForm, LoginForm
from django.views.generic import CreateView, ListView
from .models import User, Friendship
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


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


class FollowView(LoginRequiredMixin, View):

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):

        self.followee = get_object_or_404(User, username=self.kwargs["username"])
        self.follower = request.user

        if self.followee == self.follower:
            pass  # error_messagesを表示

        else:
            self.frienship = Friendship.objects.create(
                followee=self.followee,
                follower=self.follower,
            )

        return redirect("tweets:user_profile", self.frienship.followee.username)


class UnFollowView(LoginRequiredMixin, View):

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):

        self.followee = get_object_or_404(User, username=self.kwargs["username"])
        self.follower = request.user

        if self.followee == self.follower:
            pass  # error_messagesを表示

        else:
            Friendship.objects.filter(
                followee=self.followee,
                follower=self.follower,
            ).delete()

        return redirect("tweets:user_profile", self.follower.username)


class FollowingListView(ListView):
    model = Friendship
    template_name = "accounts/following_list.html"

    def get_queryset(self):
        self.follower = get_object_or_404(User, username=self.kwargs["username"])
        return Friendship.objects.filter(follower=self.follower)


class FollowerListView(ListView):
    model = Friendship
    template_name = "accounts/follower_list.html"

    def get_queryset(self):
        self.followee = get_object_or_404(User, username=self.kwargs["username"])
        return Friendship.objects.filter(followee=self.followee)
