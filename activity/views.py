from django.shortcuts import render, HttpResponse
from .models import Register
from django.utils import timezone

# Create your views here.
def register_list(request):
	return render(request, 'activity/Register.html', {})

def submit(request):
	if request.method =="POST":
		referer = request.META.get('HTTP_REFERER')	
		postBody = request.POST
		myDict = postBody.dict()
		name = myDict['name']
		companyName = myDict['companyName']
		jobTitle = myDict['jobTitle']
		mobileNo = myDict['mobileNo']
		emailAddress = myDict['emailAddress']
		print(name, companyName, jobTitle, mobileNo, emailAddress)

		Register(name=name, company_name=companyName, title=jobTitle, mobile_no=mobileNo, email_address=emailAddress, created_date=timezone.localtime(timezone.now())).save()

		return HttpResponse("Thank you for submiting the form.")
	else:
		return HttpResponse("Get")
	