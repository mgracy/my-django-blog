from django.db import models
from django.utils import timezone

# Create your models here.
class FileInfo(models.Model):
	name = models.CharField(max_length=50,null=False)
	size = models.IntegerField(False)
	downloads = models.IntegerField(default=0)
	created_date = models.DateTimeField(default=timezone.now)
	md5 = models.CharField(max_length=32, null=False)