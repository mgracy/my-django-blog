from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('create_user_profile...')
	if created:
		print('create_user_profile... created')
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('save_user_profile...')
	print(type(instance))
	# instance.UserProfile.save()
	print('save_user_profile...save_user_profile...')
