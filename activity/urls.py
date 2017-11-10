from django.conf.urls import url
from . import views

app_name = 'activity'
urlpatterns = [
    url(r'^$',views.register_list, name = 'register_list' ),
    url(r'^submit/$', views.submit),
    url(r'^consultSubmit/$', views.consultSubmit),
    url(r'^consult/$', views.consult),
    url(r'^result/$', views.result, name='register_res'),
    url(r'^report/$', views.report),
    url(r'^feedback/$', views.feedback),
    url(r'^updateActivity',views.updateActivity),
    url(r'^sendMailsForRegisters/(?P<days>[0-9])/$',views.sendMailsForRegisters),
    url(r'^sendMailsForRegistersID/(?P<pk>[0-9]+)/$',views.sendMailsForRegistersID),
    url(r'^feedback/over/$', views.feedback_over, name='feedback_over'),
    url(r'^feedback/res/$', views.feedback_result, name='feedback_res'),
    # url(r'^login/$', views.login, name='login'),
]