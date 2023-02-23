from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import User, Friendship
from .models import Tweet, Favorite
from .forms import TweetForm
from django.shortcuts import get_object_or_404


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    ordering = "-created_at"

    def get_context_data(self, **kwargs):
        queryset = Tweet.objects.select_related("author").all()
        list = Favorite.objects.select_related("tweet").filter(user=self.request.user)
        user_like_list = []
        for i in list:
            user_like_list.append(i.tweet)

        context = {
            "tweet_list": queryset,
            "user_liked_list": user_like_list,
        }

        return super().get_context_data(**context)


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

    def get_context_data(self, **kwargs):
        list = Favorite.objects.select_related("tweet").filter(user=self.request.user)
        user_like_list = []
        for i in list:
            user_like_list.append(i.tweet)

        context = {
            "user_liked_list": user_like_list,
        }

        return super().get_context_data(**context)


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
        return Tweet.objects.select_related("author").filter(author=author)

    def get_context_data(self, **kwargs):
        author = get_object_or_404(User, username=self.kwargs["username"])
        self.followee = Friendship.objects.select_related("followee").filter(
            follower=author
        )
        self.follower = Friendship.objects.select_related("follower").filter(
            followee=author
        )
        is_follow_or_not = Friendship.objects.filter(
            followee=author, follower=self.request.user
        ).exists()
        list = Favorite.objects.select_related("tweet").filter(user=self.request.user)
        user_like_list = []
        for i in list:
            user_like_list.append(i.tweet)

        context = {
            "profile": author,
            "follow_or_not": is_follow_or_not,
            "num_follows": self.followee.count(),
            "num_followers": self.follower.count(),
            "user_liked_list": user_like_list,
        }

        return super().get_context_data(**context)


class LikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        self.user = request.user

        if Favorite.objects.filter(tweet=self.tweet, user=self.user).exists():
            num_liked = (
                Favorite.objects.select_related("like").filter(tweet=self.tweet).count()
            )
            context = {
                "num_liked": num_liked,
                "tweet_pk": self.tweet.pk,
                "is_liked": True,
            }
        else:
            Favorite.objects.create(tweet=self.tweet, user=self.user)
            num_liked = (
                Favorite.objects.select_related("like").filter(tweet=self.tweet).count()
            )
            context = {
                "num_liked": num_liked,
                "tweet_pk": self.tweet.pk,
                "is_liked": True,
            }

        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        self.user = request.user

        if Favorite.objects.filter(tweet=self.tweet, user=self.user).exists():
            Favorite.objects.filter(tweet=self.tweet, user=self.user).delete()
            num_liked = (
                Favorite.objects.select_related("like").filter(tweet=self.tweet).count()
            )
            context = {
                "num_liked": num_liked,
                "tweet_pk": self.tweet.pk,
                "is_liked": False,
            }

        else:
            num_liked = (
                Favorite.objects.select_related("like").filter(tweet=self.tweet).count()
            )
            context = {
                "num_liked": num_liked,
                "tweet_pk": self.tweet.pk,
                "is_liked": False,
            }

        return JsonResponse(context)
