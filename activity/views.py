from django.shortcuts import render, HttpResponse
from .models import Register
from django.utils import timezone
import math
from .mail import SendEmail
from .sms import make_request
import activity.config

# Create your views here.
def register_list(request):
	activities = activity.config.activities
	lenAct = len(activities)
	return render(request, 'activity/Register.html', {'activities':activities, 'lenAct':lenAct})

def submit(request):
	if request.method =="POST":
		print('...begin...')
		referer = request.META.get('HTTP_REFERER')	
		postBody = request.POST
		myDict = postBody.dict()
		name = myDict[u'name']
		companyName = myDict[u'companyName']
		jobTitle = myDict[u'jobTitle']
		mobileNo = myDict['mobileNo']
		emailAddress = myDict['emailAddress']
		activityChoice = ''
		for k,v in activity.config.activities:
			if k in myDict:
				activityChoice += myDict[k] + ','

		activityChoice = activityChoice.rstrip(',')
		Register(name=name, company_name=companyName, title=jobTitle, mobile_no=mobileNo, email_address=emailAddress, created_date=timezone.localtime(timezone.now()),activities_choice=activityChoice).save()
		print('...end...')

		# sendMail
		mailFrom = activity.config.mailFrom
		mailSubject = activity.config.mailSubject
		mailBodyDear = activity.config.mailBodyDear
		mailBodyEmbedImage = activity.config.mailBodyEmbedImage
		mailBodyEmbedImagePath = activity.config.mailBodyEmbedImagePath
		mailBodySignuture = activity.config.mailBodySignuture
		msg = '{}{}{}'.format(mailBodyDear, mailBodyEmbedImage, mailBodySignuture)

		try:
			SendEmail(mailFrom, emailAddress, None, mailSubject, msg, mailBodyEmbedImagePath)
		except Exception as e:
			print('*************error**************')
			print(e)
			print('*************error**************')
			return HttpResponse(msg)
		
		print('...sendEmail end...')

		#sendSMS
		action = activity.config.smsAction
		version = activity.config.smsVersion
		regionId = activity.config.smsRegionId
		signName = activity.config.smsSignName
		templateCode = activity.config.smsTemplateCode
		topic = activity.config.topic
		user_params = {
			'Action': action, 
			"Version": version, 
			"RegionId": regionId, 			
			'PhoneNumbers': mobileNo,
			'SignName': u'{}'.format(signName),
			'TemplateCode': templateCode 
		}
		user_params['TemplateParam'] = {"time":activityChoice,"topic": topic}

		try:
			print('send SMS begin---')
			make_request(user_params)
		except Exception as e:
			print('!! send SMS eror: !!\n{}'.format(e))
		else:
			print('send SMS successfully')

		print('---send SMS over')
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