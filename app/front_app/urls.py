from django.contrib import admin
from django.urls import path, include
from app.views import *
from app.front_app import views

urlpatterns = [
    path('auth/', views.viewAuth, name='auth'),
    path('registration/', views.viewRegistration, name='registration'),
    path('profile/', views.viewProfile, name='profile'),
    path('payment/', views.viewPayment, name='payment'),
    path('withdraw/', views.viewWithdraw, name='withdraw'),
    path('operations/', views.viewOperations, name='operations'),
    path('operations/<int:id>/', views.viewOperationsDetail, name='operationsDetail'),
    path('analytic/', views.viewAnalytic, name='analytic'),
    path('', views.viewHome, name='/auth/')
] 
