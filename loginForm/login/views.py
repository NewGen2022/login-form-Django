from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.http import HttpResponseRedirect
from .authenticate import EmailAuthentication


def index(request):
    # Authenticated users view their something
    if request.user.is_authenticated:
        return render(request, "login/something.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def something(request):
    return render(request, "login/something.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            user = EmailAuthentication().authenticate(
                request, username=email, password=password
            )

            # print(user, password, email)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("something"))
            else:
                # Display error message if authentication fails
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Email and password are required.")
    else:
        form = LoginForm()

    return render(request, "login/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
    else:
        form = SignUpForm()

    return render(request, "login/signup.html", {"form": form})
