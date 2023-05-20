from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "App"

urlpatterns = [
    path("song/", views.index, name="index"),
    path("", views.index, name="index2"),
]