from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from .forms import CreateUserForm, TrafficForm
from .models import Traffic
from . import logic


def index(request):
    user = request.user

    traffic = Traffic.objects.get(pk=user.pk)

    traffic2 = {
        "from_left": request.POST.get("from_left"),
        "from_right": request.POST.get("from_right"),
        "from_top": request.POST.get("from_top"),
        "from_bottom": request.POST.get("from_bottom"),
    }
    same_value = (
        traffic.from_bottom == int(traffic2["from_bottom"])
        and traffic.from_left == int(traffic2["from_left"])
        and traffic.from_right == int(traffic2["from_right"])
        and traffic.from_top == int(traffic2["from_top"])
    )
    print(same_value)
    empty_traffic2 = (
        traffic2["from_bottom"] == None
        and traffic2["from_left"] == None
        and traffic2["from_right"] == None
        and traffic2["from_top"] == None
    )
    if same_value or empty_traffic2:
        pass
    else:
        if request.method == "POST":
            form_traffic = TrafficForm(request.POST)
            traffic.from_bottom = int(traffic2["from_bottom"])
            traffic.from_left = int(traffic2["from_left"])
            traffic.from_right = int(traffic2["from_right"])
            traffic.from_top = int(traffic2["from_top"])
            if form_traffic.is_valid():
                traffic.save()
    time_l_r, time_t_b = logic.timing_traffic_lights(traffic)

    context = {
        "form_traffic": traffic,
        "time_l_r": time_l_r,
        "time_t_b": time_t_b,
    }
    return render(request, "main/index.html", context)


@transaction.atomic  # if something wrong - nofing save to DB
def registerPage(request):
    form = CreateUserForm()
    form_traffic = TrafficForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        form_traffic = TrafficForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form_traffic.is_valid():
                traffic = form_traffic.save(commit=False)
                traffic.user_id = user.id
                traffic.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)
                return redirect("main:login")
    context = {"form": form, "form_traffic": form_traffic}
    return render(request, "main/register.html", context)


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("main:index")
        else:
            messages.info(request, "Username, email or password is wrong")

    context = {}
    return render(request, "main/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("main:login")


# def get_new_traffic(request):
#     print(request.POST)
#     print(request.method)
#     new_traffic = {
#         "from_left": request.POST.get("from_left"),
#         "from_right": request.POST.get("from_right"),
#         "from_top": request.POST.get("from_top"),
#         "from_bottom": request.POST.get("from_bottom"),
#     }
#     print(new_traffic)
#     context = {}
#     return render(request, "main/index.html", context)
