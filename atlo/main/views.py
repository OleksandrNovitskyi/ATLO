# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from .forms import CreateUserForm, TrafficForm
from .models import Traffic


def index(request):
    # user = User.objects.all()
    # form = UserForm()

    # if request.method == "POST":
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         form.save()

    # user1 = User.objects.first()
    # traffic = Traffic.objects.get(pk=user1.pk)
    # time_l_r, time_t_b = timing_traffic_lights(traffic)
    # template = loader.get_template("main/index.html")

    # context = {"form": form, "time_l_r": time_l_r, "time_t_b": time_t_b}
    context = {}
    return render(request, "main/index.html", context)
    # context = {
    #     "latest_question_list": latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))


@transaction.atomic  # if something wrong - nofing save to DB
def registerPage(request):
    form = CreateUserForm()
    form_traffic = TrafficForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        form_traffic = TrafficForm(request.POST)
        # form_traffic.user = form.id

        if form.is_valid():
            user = form.save()
            print(user)
            # form_traffic.user = user.username
            print(form_traffic.is_valid())

            for field in form_traffic:
                print("Field Error:", field.name, field.errors)

            # print(form_traffic.user_id)
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


# def create_output(input):
#     """Create files with results of calculations"""
#     traffic = input.trafic
#     time_lf_rt, time_tp_btm = timing_traffic_lights(traffic)
#     result = {"time_lf_rt": time_lf_rt, "time_tp_btm": time_tp_btm}
#     str_res = "result = " + str(result)
#     file_name = "output_{}.py".format(input.__name__[-1])
#     with open(file_name, "w", encoding="utf8") as file:
#         file.write(str_res)
