from django.forms import ModelForm
from .models import Traffic, User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class TrafficForm(ModelForm):
    class Meta:
        model = Traffic
        fields = "__all__"
