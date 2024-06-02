from django.contrib import admin
from django.urls import path, include
from app.views import *
from app.front_app import views

urlpatterns = [
    path('auth/', views.viewAuth, name='auth'),
    path('registration/', views.viewRegistration, name='registration'),
    path('', views.viewHome, name='/auth/')
]