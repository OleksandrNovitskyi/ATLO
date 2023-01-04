from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# class User(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(null=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Site user"
#         verbose_name_plural = "Site users"


class Traffic(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    from_left = models.IntegerField(default=0, null=True)
    from_right = models.IntegerField(default=0, null=True)
    from_top = models.IntegerField(default=0, null=True)
    from_bottom = models.IntegerField(default=0, null=True)

    def __str__(self):
        return (
            "from left :"
            + str(self.from_left)
            + " from right :"
            + str(self.from_right)
            + " from top :"
            + str(self.from_top)
            + " from bottom :"
            + str(self.from_bottom)
        )

    class Meta:
        verbose_name = "Traffic size"
        verbose_name_plural = "Traffic sizes"
