from django.shortcuts import render, HttpResponse
from .models import Register
from django.utils import timezone
import math
from .send_mail import sendEmail
import activity.activitiesConfig

# Create your views here.
def register_list(request):
	activities = activity.activitiesConfig.activities
	lenAct = len(activities)
	return render(request, 'activity/Register.html', {'activities':activities, 'lenAct':lenAct})

def submit(request):
	if request.method =="POST":
		print('...begin...')
		referer = request.META.get('HTTP_REFERER')	
		postBody = request.POST
		myDict = postBody.dict()
		name = myDict['name']
		companyName = myDict['companyName']
		jobTitle = myDict['jobTitle']
		mobileNo = myDict['mobileNo']
		emailAddress = myDict['emailAddress']
		print(name, companyName, jobTitle, mobileNo, emailAddress)
		print(myDict)
		activityChoice = ''
		for k,v in activity.activitiesConfig.activities:
			if k in myDict:
				activityChoice += myDict[k] + ','

		print(activityChoice)
		print('----------************--------')
		activityChoice = activityChoice.rstrip(',')
		print(activityChoice)
		print('--------************----------')
		Register(name=name, company_name=companyName, title=jobTitle, mobile_no=mobileNo, email_address=emailAddress, created_date=timezone.localtime(timezone.now()),activities_choice=activityChoice).save()
		print('...end...')
		signiture = "=================================================================\nGracy.Ma\nEmail: gx.ma@gti.com.hk\nMobile:18820036334"
		msg = "Dear {}, \nThank you for your interest in our activity. We have prepared your some amazing speech.\nBest regards,\n\n\n{}".format(name, signiture)
		try:
			sendEmail('36040944@qq.com', emailAddress, None,'This is the default mail subject', msg)
		except Exception as e:
			print('...sendEmail except...')
			msg = "Dear {}, \nthank you for submiting the form.".format(name)
			return HttpResponse(msg)
		
		print('...sendEmail end...')
		return HttpResponse(msg)
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
