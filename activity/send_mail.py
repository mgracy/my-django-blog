#coding:utf-8
import smtplib


import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import activity.activitiesConfig

smtpServer = activity.activitiesConfig.smtpServer
smtpPort = activity.activitiesConfig.smtpPort
smtpAccount = activity.activitiesConfig.smtpAccount
smtpKey = activity.activitiesConfig.smtpKey

def sendEmail(fromStr, toStr, ccStr, mailSubject, mailBody):
	msg = MIMEText(mailBody)
	print(msg)
	msg['Subject'] = mailBody
	msg['From'] = fromStr
	msg['To'] = toStr
	msg.preamble = mailSubject

	print('-----------------msg.as_string----------------:\n{}'.format(msg.as_string()))
	server = smtplib.SMTP_SSL(smtpServer, smtpPort) #实例化smtp服务器
	server.login(smtpAccount, smtpKey)
	to_list = toStr.replace("\n", "").split(',')
	print(server.sendmail(fromStr, to_list, msg.as_string()))
	print('send mail over')
	server.quit()


# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
def SendEmail(strFrom, strTo, strCc, strMailSubject, strMailBody, strMailBodyEmbedImagePath):
	# Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = strMailSubject
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	# Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText('This is the alternative plain text message.')
	msgAlternative.attach(msgText)

	# We reference the image in the IMG SRC attribute by the ID we give it below
	msgText = MIMEText(strMailBody, 'html')	
	#msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
	msgAlternative.attach(msgText)

	# This example assumes the image is in the current directory
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	print('BASE_DIR: {}'.format(BASE_DIR))
	imgs = os.path.join(BASE_DIR, strMailBodyEmbedImagePath)
	fp = open(imgs, 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	# Send the email (this example assumes SMTP authentication is required)

	server = smtplib.SMTP_SSL(smtpServer, smtpPort) #实例化smtp服务器
	server.login(smtpAccount, smtpKey)
	server.sendmail(strFrom, strTo, msgRoot.as_string())
	server.quit()
