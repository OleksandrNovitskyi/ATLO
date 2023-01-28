from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("new_traffic/", views.addNewTraffic, name="add_new_traffic"),
    path("delete_traffic/<str:pk>", views.deleteTraffic, name="delete_traffic"),
    path("activate_traffic/<str:pk>", views.activate_traffic, name="activate_traffic"),
]
