from django.shortcuts import render, HttpResponse
from .models import Register
from django.utils import timezone

# Create your views here.
def register_list(request):
	return HttpResponse('<h1>Hello world</h1>', None, '200')
