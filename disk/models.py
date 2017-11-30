from django.db import models
from django.utils import timezone

# Create your models here.
class FileInfo(models.Model):
	name = models.CharField(max_length=50,null=False)
	size = models.IntegerField(False)
	downloads = models.IntegerField(default=0)
	created_date = models.DateTimeField()
	md5 = models.CharField(max_length=32, null=False)
	user_ip = models.CharField(max_length=40, default='255.255.255.0')

class UserGPS(models.Model):
	username = models.CharField(max_length=50, null=True)
	user_ip = models.GenericIPAddressField(null=True)
	user_agent = models.CharField(max_length=200, null=True)
	lng = models.CharField(max_length=15, null=True)
	lat = models.CharField(max_length=15, null=True)
	address = models.CharField(max_length=200, null=True)
	code = models.CharField(max_length=50, null=True)
	quota = models.IntegerField(null=True)
	use = models.IntegerField(null=True)
	create_date = models.DateTimeField(auto_now_add = True, null=True)
	create_by = models.CharField(max_length=50, null=True)

	def __str__(self):
		return self.username