from django.urls import path
from . import views


urlpatterns = [
    path("", views.strongPasswordToolHome, name="strongPasswordToolHome")
]