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

# class Activity_Config(models.Model):
# 	event_organizer = models.CharField(max_length=50)
# 	organized_place = models.CharField(max_length=100)
# 	inquiries_telephone = models.CharField(max_length=20)
# 	activities_choice = models.
