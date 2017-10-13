#coding:utf-8
import smtplib

from email.mime.text import MIMEText

def sendmailMethod(temp_str=""):	
	print(temp_str)
	if temp_str:
		mailbody = temp_str
		msg = MIMEText(mailbody)
	else:
		print(4)
		textfile = 'readme.txt'
		with open(textfile) as f:
			mailbody = f.read()
			msg = MIMEText(f.read())

	fromStr = '36040944@qq.com'
	toStr = '36040944@qq.com'

	msg['Subject'] = mailbody
	msg['From'] = fromStr
	msg['To'] = toStr

	server = smtplib.SMTP_SSL("smtp.qq.com", 465) #实例化smtp服务器
	server.login(fromStr, "hnsgjollolpdbibb")
	to_list = toStr.replace("\n", "").split(',')
	server.sendmail(fromStr, to_list, msg.as_string())
	print('send mail over')
	server.quit()

def sendEmail(fromStr, toStr, ccStr, mailSubject, mailBody):
	msg = MIMEText(mailBody)
	print(msg)
	msg['Subject'] = mailBody
	msg['From'] = fromStr
	msg['To'] = toStr

	server = smtplib.SMTP_SSL("smtp.qq.com", 465) #实例化smtp服务器
	server.login(fromStr, "hnsgjollolpdbidd")
	to_list = toStr.replace("\n", "").split(',')
	print(server.sendmail(fromStr, to_list, msg.as_string()))
	print('send mail over')
	server.quit()

# if __name__ == '__main__':
# 	pass
	# sendmailMethod()
	# sendEmail('36040944@qq.com', 'mgracy3333@163.com', None, 'This is mailSubject', 'This is mail Body')	
