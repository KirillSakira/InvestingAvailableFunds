from .scripts.authorisation.login import *
from .scripts.authorisation.registration import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect

@csrf_exempt
def registration(request):
	return registrationDjango(request)

@csrf_exempt
def login(request):
	return authorisationDjango(request)


@csrf_exempt
def doLogout(request):
	logout(request)
	return redirect('/')
