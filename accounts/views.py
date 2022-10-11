from django.shortcuts import render

# Create your views here.


def SignUpView(request):
    return render(request, "accounts/signup.html", {})
