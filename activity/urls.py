from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.register_list, name = 'register_list' ),
    url(r'^submit$', views.submit),
    url(r'^result$', views.result),
]