from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Trafic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_left = models.IntegerField(default=0)
    from_right = models.IntegerField(default=0)
    from_top = models.IntegerField(default=0)
    from_bottom = models.IntegerField(default=0)

    def __str__(self):
        return (
            "from left -"
            + str(self.from_left)
            + " from right -"
            + str(self.from_right)
            + " from top -"
            + str(self.from_top)
            + " from bottom -"
            + str(self.from_bottom)
        )
