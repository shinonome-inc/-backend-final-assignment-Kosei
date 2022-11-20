from django.contrib.auth.mixins import LoginRequiredMixin

# from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import TweetModel
from .forms import TweetForm


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = TweetModel
    ordering = "-created_date"


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet.html"
    form_class = TweetForm
    model = TweetModel
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        self.tweet_obj = form.save(commit=False)
        self.tweet_obj.author = self.request.user
        self.tweet_obj.save()
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweets/detail.html"
    model = TweetModel


class TweetDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "tweets/delete.html"
    model = TweetModel
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        tweet_instance = self.get_object()
        return tweet_instance.author == self.request.user
