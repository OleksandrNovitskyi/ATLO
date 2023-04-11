from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from ..forms import CreateUserForm, TrafficForm
from ..models import Profile


@transaction.atomic  # if something wrong - nofing save to DB
def registerPage(request):
    form = CreateUserForm()
    form_traffic = TrafficForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user, image="default-user-icon-21.jpg")
            profile.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + username)
            login(request, user)
            return redirect("main:add_new_traffic")
    context = {"form": form}
    return render(request, "main/register.html", context)


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("main:index")
        else:
            messages.info(request, "Username or password is wrong")

    context = {}
    return render(request, "main/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("main:login")
