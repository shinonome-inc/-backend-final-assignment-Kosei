from .forms import AccountsForm
from django.views.generic import CreateView
from .models import User
from django.urls import reverse_lazy


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = AccountsForm
    model = User
    success_url = reverse_lazy("welcome")
