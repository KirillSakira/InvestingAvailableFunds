from .scripts.authorisation.login import *
from .scripts.authorisation.registration import *
from .scripts.OperationsWithBalance.refill import *
from .scripts.OperationsWithBalance.withdraw import *
from .scripts.clientAdd import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect

@csrf_exempt
def registration(request):
	return registrationBack(request)

@csrf_exempt
def login(request):
	return authorisationBack(request)

@csrf_exempt
def refill(request):
	return refillBack(request)

@csrf_exempt
def withdraw(request):
	return withdrawBack(request)

@csrf_exempt
def mAddClientMail(request):
	return clientAdd(request)

@csrf_exempt
def doLogout(request):
	logout(request)
	return redirect('/auth/')
