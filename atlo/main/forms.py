from django.forms import ModelForm, CharField, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Traffic


class CreateUserForm(UserCreationForm):
    attrs_input = {
        "class": "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    }
    username = CharField(widget=TextInput(attrs=attrs_input))
    email = CharField(widget=TextInput(attrs=attrs_input))
    password1 = CharField(widget=TextInput(attrs=attrs_input))
    password2 = CharField(widget=TextInput(attrs=attrs_input))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TrafficForm(ModelForm):
    attrs_input = {
        "class": "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 w-1/5 p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    }
    from_top = CharField(widget=TextInput(attrs=attrs_input))
    from_bottom = CharField(widget=TextInput(attrs=attrs_input))
    from_left = CharField(widget=TextInput(attrs=attrs_input))
    from_right = CharField(widget=TextInput(attrs=attrs_input))

    class Meta:
        model = Traffic
        fields = ["from_top", "from_bottom", "from_left", "from_right"]
