activities = (
	("cb1","11月9日9:30-12:30"),
	("cb2","11月9日14:00-17:00"),
	("cb3","11月10日9:30-12:30"),
	("cb4","11月10日14:00-17:00")
)

#mail setting
mailFrom = "36040944@qq.com"
mailSubject = u"「报名已成功 感谢您的支持！ 」"
mailBodyDear = u"您好，敬请提前十分钟到达现场进行签到。<br />交通：十号线“江湾体育场”站10号口。<br />路线图如下：<br />"
mailBodyEmbedImage = "<img src='cid:image1' />"
mailBodyEmbedImagePath = "static/images/RoadMap.jpg"
mailBodySignuture = u"<br />【GTI Shanghai】静候您的莅临，谢谢。"

#smtp settings
smtpServer = "smtp.qq.com"
smtpPort = 465
smtpAccount="36040944@qq.com"
smtpPassword=""
smtpKey="hnsgjollolpdbidd"

#sms setting
accessKeyId = 'LTAIzoK9u3s4TVGZ'
accessKeySecret = 'o9nfhyrMbOZN2NE4d9AbSwpr3FYFe5'
smsServerAddress = 'http://dysmsapi.aliyuncs.com'
smsAction = 'SendSms'
smsVersion = '2017-05-25'
smsRegionId = 'cn-hangzhou'
smsSignName = u'广州科宸电脑工程有限公司'
smsTemplateCode = 'SMS_105445037'

# notificationType
notificationType = 'MAIL'

topic = u'Security&Cloud线下场景体验活动'