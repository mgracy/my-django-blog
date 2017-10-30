from django.conf.urls import url
from . import views

app_name = 'activity'
urlpatterns = [
    url(r'^$',views.register_list, name = 'register_list' ),
    url(r'^submit/$', views.submit),
    url(r'^result/$', views.result),
    url(r'^report/$', views.report),
    url(r'^feedback/$', views.feedback),
    url(r'^feedback/over/$', views.feedback_over, name='feedback_over'),
    url(r'^feedback/res/$', views.feedback_result),
]