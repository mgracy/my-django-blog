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