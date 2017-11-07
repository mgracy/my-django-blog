from django.db import models
from django.utils import timezone

# Create your models here.
class Register(models.Model):
	name = models.CharField(max_length=50, null=False)
	company_name = models.CharField(max_length=150)
	title = models.CharField(max_length=100)
	mobile_no = models.CharField(max_length=20)
	email_address = models.CharField(max_length=50)
	created_date = models.DateTimeField(blank=True, null=True)
	activities_choice = models.CharField(max_length=100, null=True)	
	is_sendsms = models.BooleanField(default=False)

# class Activity_Config(models.Model):
# 	event_organizer = models.CharField(max_length=50)
# 	organized_place = models.CharField(max_length=100)
# 	inquiries_telephone = models.CharField(max_length=20)
# 	activities_choice = models.

class Feedback(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	advice = models.TextField()

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'published recently?'

# @python_2_unicode_compatible
class Choice(models.Model):
	question = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)	

	def __str__(self):
		return self.choice_text


class AnswerSheet(models.Model):
	ip = models.GenericIPAddressField()
	name = models.CharField(max_length=30)
	user_agent = models.CharField(max_length=150)
	question1 = models.CharField(max_length=50)
	question2 = models.CharField(max_length=50)
	question3 = models.CharField(max_length=50)
	question4 = models.CharField(max_length=50)
	question5 = models.CharField(max_length=50)
	question6 = models.CharField(max_length=50)
	question7 = models.CharField(max_length=50)
	question8 = models.CharField(max_length=50)
	question9 = models.CharField(max_length=50)
	question10 = models.CharField(max_length=50)
	advice = models.CharField(max_length=150)
	created_date = models.DateTimeField()
