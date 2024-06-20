from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name="auth"),
    path('reg/', registration, name='reg'),
    path('logout/', doLogout, name='logout'),
    path('refillBtn/', refill, name='refillBtn'),
    path('withdrawBtn/', withdraw, name='withdrawBtn'),
    path('mAddClientMail/', mAddClientMail, name='mAddClientMail'),

    path('', include('app.front_app.urls')),
]
