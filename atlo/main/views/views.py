from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from ..forms import TrafficForm, SpeedForm, ImageForm, CreateUserForm
from ..models import Traffic, Results, Speed, Profile
from .. import logic


def index(request):
    try:
        user = request.user
        traffic = Traffic.objects.filter(user=user).last()
    except TypeError:
        return redirect("main:login")
    return redirect(reverse("main:activate_traffic", args=[traffic.pk]))


def addNewTraffic(request):
    user = request.user
    form_traffic = TrafficForm()
    if request.method == "POST":
        form_traffic = TrafficForm(request.POST)
        if form_traffic.is_valid():
            traffic = form_traffic.save(commit=False)
            traffic.user_id = user.id
            traffic.save()
            return redirect("main:index")
        else:
            messages.info(request, "Username, email or password is wrong")

    context = {"form_traffic": form_traffic}
    return render(request, "main/new_traffic.html", context)


@transaction.atomic
def editAccount(request, pk):
    user = request.user
    profile = Profile.objects.get(user_id=pk)

    new_image = {"image": request.POST.get("image")}
    new_user_data = {
        "username": request.POST.get("username"),
        "email": request.POST.get("email"),
    }
    same_value = (
        (profile.image == new_image["image"])
        and (user.username == new_user_data["username"])
        and (user.email == new_user_data["email"])
    )
    form = CreateUserForm()
    image_form = ImageForm(instance=profile)
    if not same_value:
        if request.method == "POST":
            image_form = ImageForm(request.POST, request.FILES, instance=profile)
            if image_form.is_valid():
                profile.save()
                return redirect("main:index")
    context = {"image_form": image_form}
    return render(request, "main/account.html", context)


def deleteTraffic(request, pk):
    traffic = Traffic.objects.get(id=pk)
    if request.method == "POST":
        traffic.delete()
        return redirect("main:index")
    context = {"item": traffic}
    return render(request, "main/delete_traffic.html", context)


def activate_traffic(request, pk):
    traffic = Traffic.objects.get(id=pk)
    user = request.user
    traffics = Traffic.objects.filter(user=user).all()

    new_traffic = {
        "from_left": request.POST.get("from_left"),
        "from_right": request.POST.get("from_right"),
        "from_top": request.POST.get("from_top"),
        "from_bottom": request.POST.get("from_bottom"),
    }

    empty_new_traffic = (
        new_traffic["from_bottom"] is None
        or new_traffic["from_left"] is None
        or new_traffic["from_right"] is None
        or new_traffic["from_top"] is None
    )
    if not empty_new_traffic:
        same_value = (
            traffic.from_bottom == int(new_traffic["from_bottom"])
            and traffic.from_left == int(new_traffic["from_left"])
            and traffic.from_right == int(new_traffic["from_right"])
            and traffic.from_top == int(new_traffic["from_top"])
        )
    else:
        same_value = False

    if not same_value:
        if request.method == "POST":
            form_traffic = TrafficForm(request.POST)
            traffic.from_bottom = int(new_traffic["from_bottom"])
            traffic.from_left = int(new_traffic["from_left"])
            traffic.from_right = int(new_traffic["from_right"])
            traffic.from_top = int(new_traffic["from_top"])
            if form_traffic.is_valid():
                traffic.save()

    speed = Speed()
    speed_form = SpeedForm(request.POST or None)
    checkbox_chacked = False
    if request.method == "POST":
        if speed_form.is_valid():
            if "use_speed" in request.POST:
                checkbox_chacked = True
                speed, created_speed = Speed.objects.update_or_create(
                    traffic=traffic,
                    defaults={"speed": request.POST["speed"]},
                )

    time_l_r, time_t_b = logic.timing_traffic_lights(traffic)

    results, created = Results.objects.update_or_create(
        traffic=traffic,
        defaults={
            "time_lf_rt": time_l_r,
            "time_tp_bm": time_t_b,
        },
    )

    context = {
        "checkbox_chacked": checkbox_chacked,
        "speed": speed,
        "traffic": traffic,
        "traffics": traffics,
        "time_lf_rt": time_l_r,
        "time_tp_bm": time_t_b,
    }
    return render(request, "main/index.html", context)
