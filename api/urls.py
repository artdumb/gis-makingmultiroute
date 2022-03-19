
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("makeroute", views.makingrouteAPI.as_view(), name='route'),
]
