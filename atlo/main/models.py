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


class Results(models.Model):
    """Results of calculations - is time of green light in bouth direction for user"""

    traffic = models.OneToOneField(Traffic, on_delete=models.CASCADE)
    time_lf_rt = models.IntegerField()  # Time of green light in left-right direction
    time_tp_bm = models.IntegerField()  # Time of green light in top-bottom direction
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Green time from left to right : {self.time_lf_rt}, Green time from top to bottom : {self.time_tp_bm}"
