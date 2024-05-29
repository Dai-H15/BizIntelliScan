from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import secrets

# Create your views here.


def signup_view(request):
    contexts = {}
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.U_ID = secrets.token_hex(32)
            user.is_active = False
            user.save()
            contexts["U_ID"] = user.U_ID
            contexts["username"] = user.username
            return render(request, "registration/signup_done.html", contexts)

    else:
        form = SignupForm()

    param = {"form": form}

    return render(request, "registration/signup.html", param)


def done_view(request):
    pass


def policy_view(request):
    contexts = {}
    return render(request, "registration/policy.html", contexts)