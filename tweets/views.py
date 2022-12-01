from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import User
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    ordering = "-created_at"


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet.html"
    form_class = TweetForm
    model = Tweet
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        self.tweet_obj = form.save(commit=False)
        self.tweet_obj.author = self.request.user
        self.tweet_obj.save()
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweets/detail.html"
    model = Tweet


class TweetDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "tweets/delete.html"
    model = Tweet
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        tweet_instance = self.get_object()
        return tweet_instance.author == self.request.user


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "tweets/user_profile.html"
    model = Tweet
    ordering = "-created_at"

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs["username"])
        return Tweet.objects.filter(author=author)
