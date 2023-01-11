from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.registerPage, name="register"),
    path("login", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    # path("get_new_traffic/", views.get_new_traffic, name="new_traffic"),
]
