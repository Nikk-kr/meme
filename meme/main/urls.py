from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # / route
    path("register/", views.register, name="register"), # register route
    path("login/", views.login, name="login"), # login route
    path("logout/", views.logout, name="logout"), # logout route
    path("memes/", views.getmemes, name="memes"),
    path("editmeme/", views.editmeme, name="edit"),
    path("details/", views.memedetails, name="details")
]