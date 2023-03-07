from django.db import models
from django.contrib.auth.models import User


class Traffic(models.Model):
    """Number of traffic from each side for user.
    Gets from registration and changed in the main screen
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    from_left = models.IntegerField(default=0, null=True)
    from_right = models.IntegerField(default=0, null=True)
    from_top = models.IntegerField(default=0, null=True)
    from_bottom = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"from left : {self.from_left}, from right : {self.from_right}, from top : {self.from_top}, from bottom : {self.from_bottom}"

    class Meta:
        verbose_name = "Traffic size"
        verbose_name_plural = "Traffic sizes"


class OtherParam(models.Model):
    """Other parameters of calculations
    speed - Speed of cars.
    iterations - how many cycles will the traffic light work

    Added and changed in the main screen
    """

    traffic = models.OneToOneField(Traffic, on_delete=models.CASCADE)
    speed = models.IntegerField(default=60)
    iterations = models.IntegerField(default=15)

    def __str__(self):
        return f"Speed : {self.speed} km/h; Iterations : {self.iterations}"


class Results(models.Model):
    """Results of calculations - is time of green light in bouth direction for user
    and numbers of collapses in each directions

    time_lf_rt - Time of green light in left-right direction
    time_tp_bm - Time of green light in top-bottom direction
    top_collapse - number when number of cars from top direction > 1.5 * the capacity of the cross
    bottom_collapse - number when number of cars from bottom direction > 1.5 * the capacity of the cross
    left_collapse - number when number of cars from left direction > 1.5 * the capacity of the cross
    right_collapse - number when number of cars from right direction > 1.5 * the capacity of the cross
    created - date of calculation
    """

    traffic = models.OneToOneField(Traffic, on_delete=models.CASCADE)
    time_lf_rt = models.IntegerField()
    time_tp_bm = models.IntegerField()
    top_collapse = models.IntegerField()
    bottom_collapse = models.IntegerField()
    left_collapse = models.IntegerField()
    right_collapse = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Green time from left to right : {self.time_lf_rt}, Green time from top to bottom : {self.time_tp_bm}"


class Profile(models.Model):
    """User's picture"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
