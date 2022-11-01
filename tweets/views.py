from django.views.generic import TemplateView

# from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = "tweets/home.html"
    login_url = "/login/"
