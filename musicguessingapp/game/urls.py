from django.urls import path
from . import views

app_name = "App"

urlpatterns = [
    path("song/", views.index, name="index"),
    path("", views.index, name="index2"),
]