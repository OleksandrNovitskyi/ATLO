from django.forms import ModelForm, CharField, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Traffic, OtherParam, Profile

ATTRS_INPUT = {
    "class": "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
}


class CreateUserForm(UserCreationForm):

    username = CharField(widget=TextInput(attrs=ATTRS_INPUT))
    email = CharField(widget=TextInput(attrs=ATTRS_INPUT))
    password1 = CharField(widget=TextInput(attrs=ATTRS_INPUT))
    password2 = CharField(widget=TextInput(attrs=ATTRS_INPUT))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TrafficForm(ModelForm):
    from_top = CharField(widget=TextInput(attrs=ATTRS_INPUT))
    from_bottom = CharField(widget=TextInput(attrs=ATTRS_INPUT))
    from_left = CharField(widget=TextInput(attrs=ATTRS_INPUT))
    from_right = CharField(widget=TextInput(attrs=ATTRS_INPUT))

    class Meta:
        model = Traffic
        fields = ["from_top", "from_bottom", "from_left", "from_right"]


class OtherParamForm(ModelForm):
    use_speed = forms.BooleanField(required=False)
    speed = CharField(widget=TextInput(attrs=ATTRS_INPUT))
    use_iterations = forms.BooleanField(required=False)
    iterations = CharField(widget=TextInput(attrs=ATTRS_INPUT))

    class Meta:
        model = OtherParam
        fields = ["speed", "iterations"]


class ImageForm(ModelForm):
    image = CharField(
        widget=TextInput(
            attrs={
                "class": "form-control block w-full px-2 py-1 text-sm font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none",
                "type": "file",
                "id": "formFile",
            }
        )
    )

    class Meta:
        model = Profile
        fields = ["image"]
