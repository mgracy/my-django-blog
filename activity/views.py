from django.shortcuts import render, HttpResponse
from .models import Register
from django.utils import timezone
import math

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
	
def result(request):
	page = request.GET.get('page', '1')
	page = int(page)
	limit = 10
	registerTotals = Register.objects.all().order_by('-created_date')
	count = len(registerTotals)
	pages = math.ceil(count/limit)
	page = min(page, pages)
	page = max(page, 1)
	registerLists = Register.objects.all().order_by('-created_date')[(page-1)*limit:page*limit]

	context = {
		'page': page,
		'limit': limit ,
		'pages': pages,
		'count': count,
		'prevPage': '/activity/result?page='+ str(page - 1),
		'nextPage': '/activity/result?page='+ str(page + 1),
		'registerLists':registerLists
	}
		
	return render(request, 'activity/Result.html', context)

	# return render(request, 'activity/Result.html', {'registerLists':registerLists, 'context': context })

	# return render(request, 'activity/Result.html', {'registerLists':registerLists, 'page':page, 'limit':limit, 'pages':pages, 'count':count, 'prevPage':prevPage, 'nextPage':nextPage})
