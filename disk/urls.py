from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^upload/$', views.upload),
	url(r's/(\w{32})$', views.download_list),
	url(r'^files/.*?$', views.download_detail),
	url(r'^search/$', views.search),
	url(r'^gps/$', views.gps),
	url(r'^gpsimage/$', views.gpsimage),
	url(r'^location/$', views.location),
	# url(r'^files/disk/.*?$', views.download_detail)
]