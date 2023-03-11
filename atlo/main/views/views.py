from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.models import User

from ..forms import TrafficForm, OtherParamForm, ImageForm, CreateUserForm
from ..models import Traffic, Results, OtherParam, Profile
from .. import logic


def index(request):
    try:
        user = request.user
        traffic = Traffic.objects.filter(user=user).last()
    except TypeError:
        # user = User()
        # user.username = "Anonimus"
        # traffic = Traffic()
        # traffic.user_id = user.id
        # user.save()
        # traffic.save()
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

    other_param = OtherParam()
    other_param_form = OtherParamForm(request.POST or None)
    speed_checkbox_chacked = False
    iterations_checkbox_chacked = False

    if request.method == "POST":
        if other_param_form.is_valid():
            if "use_speed" in request.POST and "use_iterations" in request.POST:
                speed_checkbox_chacked = True
                iterations_checkbox_chacked = True
            elif "use_speed" in request.POST:
                speed_checkbox_chacked = True
            elif "use_iterations" in request.POST:
                iterations_checkbox_chacked = True

            other_param, created_other_param = OtherParam.objects.update_or_create(
                traffic=traffic,
                defaults={
                    "speed": speed_checkbox_chacked
                    and request.POST["speed"]
                    or other_param.speed,
                    "iterations": iterations_checkbox_chacked
                    and request.POST["iterations"]
                    or other_param.iterations,
                },
            )

    time_l_r, time_t_b = logic.get_green_signals_time(traffic)

    collapses = logic.get_collapses(traffic, other_param)

    results, created = Results.objects.update_or_create(
        traffic=traffic,
        defaults={
            "time_lf_rt": time_l_r,
            "time_tp_bm": time_t_b,
            "top_collapse": collapses["top_collapse"],
            "bottom_collapse": collapses["bottom_collapse"],
            "left_collapse": collapses["left_collapse"],
            "right_collapse": collapses["right_collapse"],
        },
    )

    context = {
        "speed_checkbox_chacked": speed_checkbox_chacked,
        "iterations_checkbox_chacked": iterations_checkbox_chacked,
        "other_param": other_param,
        "traffic": traffic,
        "traffics": traffics,
        "time_lf_rt": time_l_r,
        "time_tp_bm": time_t_b,
        "collapses": collapses,
    }
    return render(request, "main/index.html", context)
