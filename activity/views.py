from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Register, Feedback, AnswerSheet
from django.utils import timezone
from django.urls import reverse
import math
from .mail import SendEmail
from .sms import make_request
import activity.config
import activity.account
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)
now = timezone.localtime(timezone.now())
logger.debug('{}-{}:'.format(now, __name__))
# Create your views here.
def register_list(request):
	activities = activity.config.activities
	lenAct = len(activities)
	return render(request, 'activity/Register.html', {'activities':activities, 'lenAct':lenAct})

def submit(request):
	userAgent = request.META.get('HTTP_USER_AGENT')	
	if not userAgent :
		return HttpResponse('{"code":403,"desc":"Forbidden 403"}')

	if request.method =="POST":
		logger.debug('---submit main logic begin ---')
		postBody = request.POST
		myDict = postBody.dict()
		logger.debug('myDict is {}'.format(myDict))
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
		logger.debug('---submit main logic end---')

		# sendMail
		logger.debug('---submit send mail begin ---')
		mailFrom = activity.account.mailFrom
		mailSubject = activity.config.mailSubject
		mailBodyDear = activity.config.mailBodyDear.format(name)
		mailBodyEmbedImage = activity.config.mailBodyEmbedImage
		mailBodyEmbedImagePath = activity.config.mailBodyEmbedImagePath
		mailBodySignuture = activity.config.mailBodySignuture
		msg = '{}{}{}'.format(mailBodyDear, mailBodyEmbedImage, mailBodySignuture)

		try:
			SendEmail(mailFrom, emailAddress, None, mailSubject, msg, mailBodyEmbedImagePath)
		except Exception as e:
			print('*************error**************')
			print(e)
			logger.error('send mail to {} error: {}'.format(emailAddress, e))
			return HttpResponse(e)
		
		logger.debug('---submit send mail to {} end---'.format(emailAddress))

		#sendSMS
		logger.debug('---submit send sms begin ---')
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
			logger.error('send sms to {} error: {}'.format(mobileNo, e))
			print('!! send SMS eror: !!\n{}'.format(e))
			return HttpResponse(e)
		else:
			print('send SMS successfully')

		logger.debug('---submit send sms to {} over ---'.format(mobileNo))
		return render(request, 'activity/RegisterSuccess.html',{"name":name})
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
		
	return render(request, 'activity/RegisterResult.html', context)

def report(request):
	return render(request, 'activity/RegisterSuccess.html',{})	

def feedback(request):
	feedbacks = Feedback.objects.all()
	if request.method=="POST":
		try:
			postData = request.POST
			ip = get_client_ip(request)
			name = request.META.get('LOGONSERVER')
			user_agent = request.META.get('HTTP_USER_AGENT')
			question={}
			for i in range(1, len(feedbacks)):
				question[i] = postData[u'question{}'.format(i)]
			advice = postData[u'advice']
			created_date = timezone.localtime(timezone.now())
			AnswerSheet(
				ip=ip,
				name=name,
				user_agent=user_agent,
				question1=question[1],
				question2=question[2],
				question3=question[3],
				question4=question[4],
				question5=question[5],
				advice=advice,
				created_date=created_date).save()
			logger.debug("save the AnswerSheet successfully.")		
		except Exception as e:
			logger.error("save the AnswerSheet error{}.".format(e))	
			return HttpResponse('{}'.format(e))
		finally:
			return HttpResponseRedirect(reverse('activity:feedback_over'))

	else:
		return render(request, 'activity/Feedback.html', {'feedbacks':feedbacks})

def feedback_result(request):

	feedbackQuestions = Feedback.objects.all()
	answerSheets = AnswerSheet.objects.all()	

	context = {
		'feedbackQuestions':feedbackQuestions,
		'answerSheets':answerSheets
	}
		
	return render(request, 'activity/FeedbackResult.html', context)

def feedback_over(request):
	return render(request, 'activity/FeedbackSuccess.html')	

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip	