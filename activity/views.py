from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Register, Feedback, AnswerSheet, Consult
from django.utils import timezone
from django.urls import reverse
import math
from .mail import SendEmail
from .sms import make_request
import activity.config
import activity.account
import logging
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import time

logger = logging.getLogger(__name__)
now = timezone.localtime(timezone.now())
logger.debug('{}-{}:'.format(now, __name__))
# Create your views here.
def register_list(request):
	activities = activity.config.activities
	lenAct = len(activities)
	return render(request, 'activity/Register.html', {'activities':activities, 'lenAct':lenAct})

def registerSubmit(request):
	userAgent = request.META.get('HTTP_USER_AGENT')	
	if not userAgent :
		return HttpResponse('{"code":403,"desc":"Forbidden 403"}')

	if request.method =="POST":
		logger.debug('---submit main logic begin -{}--'.format(timezone.localtime(timezone.now())))
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

		try:
			print('send SMS begin---')
			templateCode = activity.config.smsConsultTemplateCode
			user_params = build_user_params(mobileNo, activityChoice, templateCode)
			obj = make_request(user_params)
			logger.debug('send sms to, response from sms interface is {}'.format(obj))
		except Exception as e:
			logger.error('send sms to {} error: {}'.format(mobileNo, e))
			print('!! send SMS eror: !!\n{}'.format(e))
			return HttpResponse(e)
		else:
			print('send SMS successfully')

		logger.debug('---submit send sms to {} over -{}--'.format(mobileNo, timezone.localtime(timezone.now())))
		return render(request, 'activity/RegisterSuccess.html',{"name":name})
	else:
		return HttpResponse("Get")

@login_required
def registerResult(request):
	userInfo = request.user
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
		'prevPage': '/activity/register/res?page='+ str(page - 1),
		'nextPage': '/activity/register/res?page='+ str(page + 1),
		'registerLists':registerLists,
		'userInfo': userInfo
	}
		
	return render(request, 'activity/RegisterResult.html', context)

def registerOver(request):
	return render(request, 'activity/RegisterSuccess.html',{})

def consult(request):
	return render(request, 'activity/Consult.html')

def consultSubmit(request):
	userAgent = request.META.get('HTTP_USER_AGENT')	
	if not userAgent :
		return HttpResponse('{"code":403,"desc":"Forbidden 403"}')

	if request.method =="POST":
		logger.debug('---submit main logic begin -{}--'.format(timezone.localtime(timezone.now())))
		postBody = request.POST
		myDict = postBody.dict()
		logger.debug('myDict is {}'.format(myDict))
		name = myDict[u'name']
		companyName = myDict[u'companyName']
		mobileNo = myDict['mobileNo']
		emailAddress = myDict['emailAddress']
		questions = myDict['questions']
		userAgent = request.META.get("HTTP_USER_AGENT")
		ip = get_client_ip(request)

		Consult(name=name, company_name=companyName, mobile_no=mobileNo, email_address=emailAddress, created_date=timezone.localtime(timezone.now()),questions=questions, ip=ip, user_agent=userAgent).save()
		logger.debug('---submit main logic end---')

		# sendMail
		logger.debug('---submit send mail begin ---')
		mailFrom = activity.account.mailFrom
		mailSubject = activity.config.consult_mailSubject
		mailBodyDear = activity.config.consult_mailBodyDear.format(name)
		mailBodyEmbedImage = activity.config.consult_mailBodyEmbedImage
		mailBodyEmbedImagePath = activity.config.consult_mailBodyEmbedImagePath
		mailBodySignuture = activity.config.consult_mailBodySignuture
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

		try:
			print('send SMS begin---')
			templateCode = activity.config.smsConsultTemplateCode
			user_params = build_user_params(mobileNo, '', templateCode)
			obj = make_request(user_params)
			logger.debug('send sms to, response from sms interface is {}'.format(obj))
		except Exception as e:
			logger.error('send sms to {} error: {}'.format(mobileNo, e))
			print('!! send SMS eror: !!\n{}'.format(e))
			return HttpResponse(e)
		else:
			print('send SMS successfully')

		logger.debug('---submit send sms to {} over -{}--'.format(mobileNo, timezone.localtime(timezone.now())))
		return render(request, 'activity/ConsultSuccess.html',{"name":name})
	else:
		return HttpResponse("Get")

def consultOver(request):
	return render(request, 'activity/ConsultSuccess.html',{})

@login_required
def consultResult(request):
	userInfo = request.user
	page = request.GET.get('page', '1')
	page = int(page)
	limit = 10
	consultTotals = Consult.objects.all().order_by('-created_date')
	count = len(consultTotals)
	pages = math.ceil(count/limit)
	page = min(page, pages)
	page = max(page, 1)
	consults = Consult.objects.all().order_by('-created_date')[(page-1)*limit:page*limit]

	context = {
		'page': page,
		'limit': limit ,
		'pages': pages,
		'count': count,
		'prevPage': '/activity/consult/res?page='+ str(page - 1),
		'nextPage': '/activity/consult/res?page='+ str(page + 1),
		'consults':consults,
		'userInfo': userInfo
	}
		
	return render(request, 'activity/ConsultResult.html', context)	

def feedback(request):
	feedbacks = Feedback.objects.all()
	if request.method=="POST":
		try:
			postData = request.POST
			ip = get_client_ip(request)
			name = request.META.get('LOGONSERVER') 
			if name == None or name == "":
				name = 'guest'
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

@login_required
def feedback_result(request):
	userInfo = request.user
	feedbackQuestions = Feedback.objects.all()
	answerSheets = AnswerSheet.objects.all()	

	context = {
		'feedbackQuestions':feedbackQuestions,
		'answerSheets':answerSheets,
		'userInfo': userInfo
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

def updateActivity(request):
	if request.method == "POST":
		httpReferer = request.META.get("HTTP_REFERER")
		userAgent = request.META.get("HTTP_USER_AGENT")
		if httpReferer and userAgent:
			dicts = dict(request.POST)
			for key in dicts.keys():
				if key.find('cxSMS') >= 0:
					id = key.replace('cxSMS','')
					register = Register.objects.get(id=id)
					register.is_sendsms = True
					register.save()
				else:
					pass

			return HttpResponse('{"status":200}')
		else:
			return HttpResponse('{"status":403, "text":"Forbidden"}')					

	else:
		return HttpResponse('{"status":403, "text":"Forbidden"}')

@login_required
def sendMailsForRegisters(request, days=1):
	'''
	This method will automatically send sms to those whom have registered with the field is_sendsms = True.
	The logic is system would send sms to user automatically days ahead.
	'''
	days = int(days)
	registers = Register.objects.filter(is_sendsms = True)

	totals = len(registers)
	i = 0
	month = timezone.now().month
	day = timezone.now().day
	for register in registers:
		mobileNo = register.mobile_no
		activityChoice = register.activities_choice
		listChoices = activityChoice.split(',')
		for listChoice in listChoices:
			strDate = listChoice.split(' ')[0]
			str2Date = time.strptime(strDate, u'%m月%d日')
			if month == str2Date.tm_mon and day + days == str2Date.tm_mday:
				logger.debug('---sendMailsForRegisters send sms begin --{}-{}'.format(i, mobileNo))
				user_params = build_user_params(mobileNo, activityChoice)
				try:
					print('send SMS begin---{}'.format(mobileNo))
					obj = make_request(user_params)
					logger.debug('send sms to, response from sms interface is {}'.format(obj))
				except Exception as e:
					logger.error('send sms to {} error: {}'.format(mobileNo, e))
					print('!! send SMS eror: !!\n{}'.format(e))
					return HttpResponse(e)
				else:
					i += 1
					print('send SMS successfully {}-{}'.format(i, mobileNo))
					logger.debug('---sendMailsForRegisters send sms end --{}-{}'.format(i, mobileNo))
				break
			else:
				continue			

	msg = 'send SMS successfully {}/{}'.format(i, totals)
	print(msg)
	logger.debug(msg)
	response = {
		"status": 200,
		"text": msg
	}

	return HttpResponse(str(response).replace("'",'"'))

@login_required
def sendMailsForRegistersID(request, pk):
	registers = Register.objects.filter(is_sendsms = True).filter(id=pk)

	totals = len(registers)
	i = 0
	for register in registers:
		mobileNo = register.mobile_no
		activityChoice = register.activities_choice
		
		logger.debug('---sendMailsForRegisters send sms begin ---')
		user_params = build_user_params(mobileNo, activityChoice)
		try:
			print('send SMS begin---{}'.format(mobileNo))
			obj = make_request(user_params)
			logger.debug('send sms to, response from sms interface is {}'.format(obj))
		except Exception as e:
			logger.error('send sms to {} error: {}'.format(mobileNo, e))
			print('!! send SMS eror: !!\n{}'.format(e))
			return HttpResponse(e)
		else:
			i += 1
			print('send SMS successfully {}-{}'.format(i, mobileNo))

	msg = 'send SMS successfully {}/{}-{}'.format(i, totals, pk)
	print(msg)
	logger.debug(msg)
	response = {
		"status": 200,
		"text": msg
	}

	return HttpResponse(str(response).replace("'",'"'))

def build_user_params(mobileNo, activityChoice, templateCode):
	action = activity.config.smsAction
	version = activity.config.smsVersion
	regionId = activity.config.smsRegionId
	signName = activity.config.smsSignName
	templateCode = templateCode
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

	return user_params	