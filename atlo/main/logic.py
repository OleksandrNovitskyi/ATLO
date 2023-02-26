import random
import math

MAX_CYCLE_TIME = 120
S = 25  # length of cross
a = 1.5  # acceleration of the car
SPEED = 60  # km/h


def get_green_signals_time(traff):
    """traffic - instance of the class Traffic. Consist of traffic number in each line

    return green time at horizontal line (left-right), green time at vertical line (top-bottom)
    """
    yellow_time = 3  # yellow time

    max_traf_l_r = max(traff.from_left, traff.from_right)
    max_traf_t_b = max(traff.from_top, traff.from_bottom)

    time_l_r = (
        max_traf_l_r * (MAX_CYCLE_TIME - yellow_time) // (max_traf_l_r + max_traf_t_b)
    )

    if time_l_r < 15:
        time_l_r = 15
    time_t_b = (MAX_CYCLE_TIME - yellow_time) - time_l_r
    if time_t_b < 15:
        time_t_b = 15
    time_l_r = (MAX_CYCLE_TIME - yellow_time) - time_t_b
    return time_l_r, time_t_b


def get_time_to_stop(speed):
    """Get time wich is needed for car to stop"""
    speed_mps = speed * 1000 / 3600
    braking_distance = speed_mps * speed_mps / (2 * 9.81 * 0.7)  # d=(v^2)/2gµ
    time_to_stop = math.sqrt(2 * braking_distance / 9.81)  # t=sqrt(2d/a)
    return time_to_stop


def generate_time_for_every_car(traff_from):
    list_time_new_cars = []
    for i in range(traff_from):
        start_second = random.randint(1, MAX_CYCLE_TIME)
        while start_second in list_time_new_cars:
            start_second += 0.3
        list_time_new_cars.append(start_second)
    list_time_new_cars = sorted(list_time_new_cars)
    return list_time_new_cars


def current_line(traff_from, green_time, curr_line, time_when_last_car_starts):
    """Get number of cars wich stop in line"""

    left_turn_percent = {
        "perc_left": 0.2,
        "perc_right": 0.25,
        "perc_top": 0.01,
        "perc_bottom": 0,
    }
    # list with time of all cars wich ride from some side
    list_time_new_cars = generate_time_for_every_car(traff_from)

    capacity = get_cross_capacity(green_time)  # capacity of cross(number of cars)
    time_to_stop = get_time_to_stop(SPEED)

    numb_cars = 0
    period_time_to_leave_cross = 0
    stay_cars_list = []  # list with time of cars what don't out of cross
    if curr_line > capacity + 5:
        curr_line = curr_line - capacity + traff_from
    else:
        for start_second in list_time_new_cars:
            stay_condition = (
                start_second + period_time_to_leave_cross > green_time - time_to_stop
            )

            if start_second < time_when_last_car_starts:
                time_when_last_car_starts += math.sqrt(2 * 4.5 / a)
                numb_cars += 1
                period_time_to_leave_cross = math.sqrt(
                    2 * (curr_line + numb_cars) * 4.5 / a + 1 * (curr_line + numb_cars)
                )
                if stay_condition:
                    stay_cars_list.append(start_second)
            elif start_second < (
                time_when_last_car_starts + period_time_to_leave_cross
            ):
                period_time_to_leave_cross += math.sqrt(2 * 4.5 / a)
                if stay_condition:
                    stay_cars_list.append(start_second)
            else:
                if stay_condition:
                    stay_cars_list.append(start_second)

        curr_line = len(stay_cars_list)

    # print(stay_cars_list)
    return curr_line


def get_cross_capacity(green_time):
    """Get number of cars wich can out of cross when they starts from congestion"""
    time_to_leave = math.sqrt(2 * S / a)
    capacity = int((green_time - time_to_leave) / (math.sqrt(2 * 4.5 / a) + 1) + 1)
    return capacity


def get_time_when_last_car_starts(curr_line_len):
    if curr_line_len > 0:
        result = (math.sqrt(2 * 4.5 / a) + 1) * (curr_line_len - 1) + 1
    else:
        result = 0
    return result


def get_collapses(traffic, other_param):
    """
    traffic - instance of the class Traffic. Consist of traffic number in each line
    speed - instance of the class Speed. Consist a speed of traffic

    return dictionary with number of vertical and horisontal collapses
    """
    global SPEED

    if other_param.speed:
        SPEED = int(other_param.speed)
    iter = 10
    if other_param.iterations:
        iter = int(other_param.iterations)
    collapses = {
        "top collapse": 0,
        "bottom collapse": 0,
        "left collapse": 0,
        "right collapse": 0,
    }
    time_l_r, time_t_b = get_green_signals_time(traffic)
    # print(time_l_r, time_t_b)
    if time_l_r > time_t_b:  # horizontal green
        curr_left_line = 0
        curr_right_line = 0
        curr_top_line = traffic.from_top * time_l_r // MAX_CYCLE_TIME
        curr_bottom_line = traffic.from_bottom * time_l_r // MAX_CYCLE_TIME
    else:  # vertical green
        curr_left_line = traffic.from_left * time_t_b // MAX_CYCLE_TIME
        curr_right_line = traffic.from_right * time_t_b // MAX_CYCLE_TIME
        curr_top_line = 0
        curr_bottom_line = 0

    for i in range(iter):
        time_when_starts_last_left = get_time_when_last_car_starts(curr_left_line)
        curr_left_line = current_line(
            traffic.from_left, time_l_r, curr_left_line, time_when_starts_last_left
        )
        if time_when_starts_last_left > time_l_r * 1.5:
            collapses["left collapse"] += 1

        time_when_starts_last_right = get_time_when_last_car_starts(curr_right_line)
        curr_right_line = current_line(
            traffic.from_right,
            time_l_r,
            curr_right_line,
            time_when_starts_last_right,
        )
        if time_when_starts_last_right > time_l_r * 1.5:
            collapses["right collapse"] += 1

        time_when_starts_last_top = get_time_when_last_car_starts(curr_top_line)
        curr_top_line = current_line(
            traffic.from_top, time_t_b, curr_top_line, time_when_starts_last_top
        )
        if time_when_starts_last_top > time_t_b * 1.5:
            collapses["top collapse"] += 1

        time_when_starts_last_bottom = get_time_when_last_car_starts(curr_bottom_line)
        curr_bottom_line = current_line(
            traffic.from_bottom,
            time_t_b,
            curr_bottom_line,
            time_when_starts_last_bottom,
        )
        if time_when_starts_last_bottom > time_t_b * 1.5:
            collapses["bottom collapse"] += 1
    print(SPEED)
    print(iter)
    return collapses
