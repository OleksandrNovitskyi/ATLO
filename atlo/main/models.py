from django.db import models
from django.contrib.auth.models import User


class Traffic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    from_left = models.IntegerField(default=0, null=True)
    from_right = models.IntegerField(default=0, null=True)
    from_top = models.IntegerField(default=0, null=True)
    from_bottom = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"from left : {str(self.from_left)}, from right : {str(self.from_right)}, from top : {str(self.from_top)}, from bottom : {str(self.from_bottom)}"

    class Meta:
        verbose_name = "Traffic size"
        verbose_name_plural = "Traffic sizes"


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_lf_rt = models.IntegerField()  # Time of green light in left-right direction
    time_tp_bm = models.IntegerField()  # Time of green light in top-bottom direction
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Green time from left to right : {str(self.time_lf_rt)}, Green time from top to bottom : {str(self.time_tp_bm)}"
