from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello world!!!1")

def profileController(request, username):
	response = "Gledas profile uporabnika z imenom: %s."
	return HttpResponse(response % username)

def tagController(request, tagname):
	response = "Gledas tag z imenom: %s."
	return HttpResponse(response % tagname)

def loginController(request):
	response = "Gledas login formo"
	return HttpResponse(response)

def registerController(request):
	response = "Gledas register formo"
	return HttpResponse(response)