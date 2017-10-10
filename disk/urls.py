from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^upload/$', views.upload),
	url(r's/(\w{32})$', views.download_list),
	url(r'^files/disk/.*?$', views.download_detail)
]