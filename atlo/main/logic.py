import random
import math

MAX_CYCLE_TIME = 120
S = 25  # length of cross
acceleration = 1.5  # acceleration of the car
SPEED = 60  # km/h
left_turn_percent = {
    "perc_left": 0.2,
    "perc_right": 0.25,
    "perc_top": 0.01,
    "perc_bottom": 0,
}


class Car:
    """Represents a car."""

    def __init__(self, time, left_turn=False):
        self.time = time
        self.left_turn = left_turn

    def __str__(self):
        """Returns a human-readable string representation."""
        return f"Time when car enter to the cross - {self.time}"


class Direction:
    """Represents a list of cars from some direction.

    Attributes:
      cars: list of Car objects.
      cars_time_list: list of Car.time
    """

    def __init__(self, direction_traffic, turn_left_percent):
        """Initializes the Direction with n cars."""
        self.cars = []
        self.cars_time_list = []
        for start_second in range(direction_traffic):
            start_second = random.randint(1, MAX_CYCLE_TIME)
            for car1 in self.cars:
                self.cars_time_list.append(car1.time)
            while start_second in self.cars_time_list:
                start_second += 0.25
            car = Car(start_second, probably(turn_left_percent))
            self.cars.append(car)
        self.sort()

    def __str__(self):
        """Returns a string representation of the deck."""
        res = []
        for car in self.cars:
            res.append(str(car))
        return "\n".join(res)

    def sort(self):
        """Sorts the cars in ascending order."""
        self.cars.sort(key=lambda x: x.time, reverse=False)

    def add_car(self, car_obj):
        """Add one car to the direction.

        car_obj: Car
        """
        new_car = Car(0, car_obj.left_turn)
        while (new_car.time in self.cars_time_list) or (
            float(new_car.time) in self.cars_time_list
        ):
            new_car.time += 0.25
        self.cars.append(new_car)
        self.cars_time_list.append(new_car.time)
        self.sort()

    def add_cars(self, prev_direction):
        """Add line of cars to the direction.

        prev_direction: Direction
        """
        for car in prev_direction.cars:
            car.time = 0
            while (car.time in self.cars_time_list) or (
                float(car.time) in self.cars_time_list
            ):
                car.time += 0.25
            self.cars.append(car)
            self.cars_time_list.append(car.time)
        self.sort()

    def remove_car(self, time_to_out):
        """Removes cars from the direction wich time less than time_to_out

        time_to_out: integer
        """
        self.cars = [car for car in self.cars if car.time > time_to_out]

    def remove_n_car(self, number):
        """Removes n first cars from the direction

        number: integer
        """
        del self.cars[:number]

    def get_length(self):
        """len() function"""
        return len(self.cars)

    def find_first_turnd_left(self):
        """Find first car in the Direction what will turn left"""
        for car in self.cars:
            if car.left_turn:
                return car

    def next(self, car_obj):
        """Return next car of the direction"""
        for car in self.cars:
            if car.time > car_obj.time:
                return car


def probably(chance):
    return random.random() < chance


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


def get_cross_capacity(green_time):
    """Get number of cars wich can out of cross when they starts from congestion"""
    time_to_leave = math.sqrt(2 * S / acceleration)
    capacity = int(
        (green_time - time_to_leave) / (math.sqrt(2 * 4.5 / acceleration) + 1) + 1
    )
    return capacity


def current_line(
    traff_from, left_turn_perc, green_time, curr_direction, time_when_last_car_starts
):
    """Get number of cars wich stop in line"""
    new_cars = Direction(traff_from, left_turn_perc)
    capacity = get_cross_capacity(green_time)  # capacity of cross(number of cars)
    time_to_stop = get_time_to_stop(SPEED)
    curr_line = curr_direction.get_length()
    numb_cars = 0
    period_time_to_leave_cross = 0

    new_cars_wich_stay = Direction(0, 0)

    if curr_line > capacity + 5:
        new_cars.add_cars(curr_direction)
        new_cars.sort()
        new_cars.remove_n_car(capacity)
        new_cars_wich_stay = new_cars

    else:
        for car in new_cars.cars:
            stay_condition = (
                car.time + period_time_to_leave_cross > green_time - time_to_stop
            )
            if car.time < time_when_last_car_starts:
                time_when_last_car_starts += math.sqrt(2 * 4.5 / acceleration)
                numb_cars += 1
                period_time_to_leave_cross = math.sqrt(
                    2 * (curr_line + numb_cars) * 4.5 / acceleration
                    + 1 * (curr_line + numb_cars)
                )
                if stay_condition:
                    new_cars_wich_stay.add_car(car)
            elif car.time < (time_when_last_car_starts + period_time_to_leave_cross):
                period_time_to_leave_cross += math.sqrt(2 * 4.5 / acceleration)
                if stay_condition:
                    new_cars_wich_stay.add_car(car)
            else:
                if stay_condition:
                    new_cars_wich_stay.add_car(car)
    return new_cars_wich_stay


def get_time_when_last_car_starts(curr_line_obj):
    curr_line = curr_line_obj.get_length()
    if curr_line > 0:
        result = (math.sqrt(2 * 4.5 / acceleration) + 1) * (curr_line - 1) + 1
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
    if other_param.iterations:
        iter = int(other_param.iterations)
    collapses = {
        "top collapse": 0,
        "bottom collapse": 0,
        "left collapse": 0,
        "right collapse": 0,
    }
    time_l_r, time_t_b = get_green_signals_time(traffic)
    if time_l_r > time_t_b:  # horizontal green
        curr_left_line = Direction(0, 0)
        curr_right_line = Direction(0, 0)
        curr_top_line = Direction(
            traffic.from_top * time_l_r // MAX_CYCLE_TIME, left_turn_percent["perc_top"]
        )
        curr_bottom_line = Direction(
            traffic.from_bottom * time_l_r // MAX_CYCLE_TIME,
            left_turn_percent["perc_bottom"],
        )
    else:  # vertical green
        curr_left_line = Direction(
            traffic.from_left * time_t_b // MAX_CYCLE_TIME,
            left_turn_percent["perc_left"],
        )
        curr_right_line = Direction(
            traffic.from_right * time_t_b // MAX_CYCLE_TIME,
            left_turn_percent["perc_right"],
        )
        curr_top_line = Direction(0, 0)
        curr_bottom_line = Direction(0, 0)

    for i in range(iter):
        time_when_starts_last_left = get_time_when_last_car_starts(curr_left_line)
        time_when_starts_last_right = get_time_when_last_car_starts(curr_right_line)
        curr_left_line = current_line(
            traffic.from_left,
            left_turn_percent["perc_left"],
            time_l_r,
            curr_left_line,
            time_when_starts_last_left,
        )
        curr_right_line = current_line(
            traffic.from_right,
            left_turn_percent["perc_right"],
            time_l_r,
            curr_right_line,
            time_when_starts_last_right,
        )

        if time_when_starts_last_left > time_l_r * 1.5:
            collapses["left collapse"] += 1
        if time_when_starts_last_right > time_l_r * 1.5:
            collapses["right collapse"] += 1

        time_when_starts_last_top = get_time_when_last_car_starts(curr_top_line)
        curr_top_line = current_line(
            traffic.from_top,
            left_turn_percent["perc_top"],
            time_t_b,
            curr_top_line,
            time_when_starts_last_top,
        )
        if time_when_starts_last_top > time_t_b * 1.5:
            collapses["top collapse"] += 1

        time_when_starts_last_bottom = get_time_when_last_car_starts(curr_bottom_line)
        curr_bottom_line = current_line(
            traffic.from_bottom,
            left_turn_percent["perc_bottom"],
            time_t_b,
            curr_bottom_line,
            time_when_starts_last_bottom,
        )
        if time_when_starts_last_bottom > time_t_b * 1.5:
            collapses["bottom collapse"] += 1
    return collapses


if __name__ == "__main__":

    direction = Direction(5, 0.03)
    direction.sort()
    direction2 = Direction(4, 0.2)
    print(direction)
    print()
    car = Car(24)
    car2 = Car(24)
    direction.add_car(car)
    direction.add_car(car2)
    direction.add_car(car)
    car = direction.find_first_turnd_left()
    print(car)
