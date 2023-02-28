from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView
from .forms import TweetForm
from .models import Favorite, Tweet


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    ordering = "-created_at"
    queryset = Tweet.objects.all().select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_like_list = (
            Favorite.objects.select_related("tweet")
            .filter(user=self.request.user)
            .values_list("tweet", flat=True)
        )
        context["user_liked_list"] = user_like_list
        print(user_like_list)

        return context


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
        context = super().get_context_data(**kwargs)
        user_like_list = (
            Favorite.objects.select_related("tweet")
            .filter(tweet=self.object, user=self.request.user)
            .values_list("tweet", flat=True)
        )
        context["user_liked_list"] = user_like_list
        return context


class TweetDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "tweets/delete.html"
    model = Tweet
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        tweet_instance = self.get_object()
        return tweet_instance.author == self.request.user


class LikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        user = request.user
        Favorite.objects.get_or_create(tweet=tweet, user=user)
        num_liked = tweet.favorite_tweet.count()
        context = {
            "num_liked": num_liked,
            "tweet_pk": tweet.pk,
            "is_liked": True,
        }
        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        user = request.user
        if Favorite.objects.filter(tweet=tweet, user=user).exists():
            Favorite.objects.filter(tweet=tweet, user=user).delete()
        num_liked = tweet.favorite_tweet.count()
        context = {
            "num_liked": num_liked,
            "tweet_pk": tweet.pk,
            "is_liked": False,
        }
        return JsonResponse(context)
