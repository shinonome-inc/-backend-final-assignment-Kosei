from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from tweets.models import Favorite, Tweet

from .forms import AccountsForm, LoginForm
from .models import Friendship, User


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
            messages.add_message(request, messages.ERROR, "自分自身のことはフォローできません。")
            return render(request, "tweets/home.html")

        elif Friendship.objects.filter(
            followee=self.followee, follower=self.follower
        ).exists():
            messages.add_message(request, messages.ERROR, "このユーザーはすでにフォロー済みです")
            return render(request, "tweets/home.html")

        else:
            self.friendship = Friendship.objects.create(
                followee=self.followee,
                follower=self.follower,
            )
            return redirect("tweets:home")


class UnFollowView(LoginRequiredMixin, View):

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):

        self.followee = get_object_or_404(User, username=self.kwargs["username"])
        self.follower = request.user

        if self.followee == self.follower:
            messages.add_message(request, messages.ERROR, "自分自身のことはアンフォローできません。")
            return render(request, "tweets/home.html")

        else:
            Friendship.objects.filter(
                followee=self.followee,
                follower=self.follower,
            ).delete()
            return redirect("tweets:home")


class FollowingListView(ListView):
    model = Friendship
    template_name = "accounts/following_list.html"

    def get_queryset(self):

        self.follower = get_object_or_404(User, username=self.kwargs["username"])

        return Friendship.objects.select_related("follower").filter(
            follower=self.follower
        )


class FollowerListView(ListView):
    model = Friendship
    template_name = "accounts/follower_list.html"

    def get_queryset(self):

        self.followee = get_object_or_404(User, username=self.kwargs["username"])

        return Friendship.objects.select_related("followee").filter(
            followee=self.followee
        )


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/user_profile.html"
    model = Tweet
    ordering = "-created_at"

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs["username"])
        return Tweet.objects.select_related("author").filter(author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs["username"])
        followee = Friendship.objects.select_related("followee").filter(follower=author)
        follower = Friendship.objects.select_related("follower").filter(followee=author)
        is_follow_or_not = Friendship.objects.filter(
            followee=author, follower=self.request.user
        ).exists()
        user_like_list = (
            Favorite.objects.select_related("tweet")
            .filter(user=self.request.user)
            .values_list("tweet", flat=True)
        )
        context["profile"] = author
        context["follow_or_not"] = is_follow_or_not
        context["num_follows"] = followee.count()
        context["num_followers"] = follower.count()
        context["user_liked_list"] = user_like_list
        return context
