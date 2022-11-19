from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import TweetForm
from .models import TweetModel


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"


class TweetCreateView(CreateView):
    template_name = "tweets/tweet.html"
    form_class = TweetForm
    model = TweetModel
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        self.tweet = form.save(commit=False)
        self.tweet.author = self.request.user
        self.tweet.save()
        return super().form_valid(form)
