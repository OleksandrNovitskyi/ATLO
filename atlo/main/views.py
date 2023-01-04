# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect

from .forms import UserForm
from .models import User, Traffic


def index(request):
    # user = User.objects.all()
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

    user1 = User.objects.first()
    traffic = Traffic.objects.get(pk=user1.pk)
    time_l_r, time_t_b = timing_traffic_lights(traffic)
    # template = loader.get_template("main/index.html")

    context = {"form": form, "time_l_r": time_l_r, "time_t_b": time_t_b}
    return render(request, "main/index.html", context)
    # context = {
    #     "latest_question_list": latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))


def register(request):
    user = {request.POST.get("login"): request.POST.get("email")}
    return user


def get_traffic(request):
    traf = {
        "from_left": request.POST.get("from_left"),
        "from_right": request.POST.get("from_right"),
        "from_top": request.POST.get("from_top"),
        "from_bottom": request.POST.get("from_bottom"),
    }
    return traf


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
