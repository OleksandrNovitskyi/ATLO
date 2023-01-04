# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import TrafficForm, CreateUserForm
from .models import Traffic


def index(request):
    # user = User.objects.all()

    user1 = User.objects.first()
    traffic = Traffic.objects.get(pk=user1.pk)
    time_l_r, time_t_b = timing_traffic_lights(traffic)

    context = {"time_l_r": time_l_r, "time_t_b": time_t_b, "traffic": traffic}
    return render(request, "main/index.html", context)


def login(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    context = {"form": form}

    return render(request, "main/login.html", context)


def register(request):
    form = CreateUserForm()
    form_tr = TrafficForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        form_tr = TrafficForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            if form_tr.is_valid():
                form_tr.save()
                form.save()
                return redirect("index")

    context = {"form": form, "form_tr": form_tr}

    return render(request, "main/register.html", context)


def timing_traffic_lights(traffic):
    """
    traffic - QuerySet of traffic number in each lane

    return green time at line left-righr, green time at line top-bottom
    """
    max_cycle_time = 120
    sum_traf_l_r = traffic.from_left + traffic.from_right
    sum_traf_t_b = traffic.from_top + traffic.from_bottom

    time_l_r = sum_traf_l_r * max_cycle_time // (sum_traf_l_r + sum_traf_t_b)
    if time_l_r < 15:
        time_l_r = 15
    time_t_b = max_cycle_time - time_l_r

    return time_l_r, time_t_b
