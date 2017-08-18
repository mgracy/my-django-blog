from django.db import models

# Create your models here.

from django.utils import timezone

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	create_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		print(1)
		print(type(self))
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		print('__str__ is calling')
		return self.title
