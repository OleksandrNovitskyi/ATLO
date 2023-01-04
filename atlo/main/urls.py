from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.registerPage, name="register"),
    path("login", views.loginPage, name="login"),
]
