from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

def index(request):
	return HttpResponse('<h1>Index</h1>')

def finduser(request):
	print(3333333333333333333333333)
	user = User.objects.filter(username=request.GET['username'])	
	if user:
		return HttpResponse("{'code':200,'text':'the account is exists.'}")
	else:
		return HttpResponse("{'code':404,'text':'the account is not exists.'}")

def login(request):
	if request.user.is_authenticated(): 
		return HttpResponseRedirect('/')

	if request.method =="POST":
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
	    
		user = auth.authenticate(username=username, password=password)

		if user is not None and user.is_active:
			auth.login(request, user)
			forward_url = '/'
			if request.GET:
				forward_url = request.GET['next']
			return HttpResponseRedirect(forward_url)
		else:
			message = 'We didn’t recognize that password.'
			return render(request, 'activity/login.html', {'message':message})

	else:
		return render(request, 'activity/login.html', {})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/index/')

