from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .regModule import returnJson

def authorisationDjango(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return returnJson(status='success')
	return returnJson(status='Error', message='Неверный логин или пароль')