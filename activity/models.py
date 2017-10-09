from django.db import models
from django.utils import timezone

# Create your models here.
class Register(models.Model):
	name = models.ForeignKey('auth.User')
	company_name = models.CharField(max_length=150)
	title = models.CharField(max_length=100)
	mobile_no = models.CharField(max_length=20)
	email_address = models.CharField(max_length=50)
	created_date = models.DateTimeField(blank=True, null=True)

	def submit(self):
		self.created_date = timezone.now()
		self.save()

	def __str__(self):
		return str(self.name) + ' ' + self.title		