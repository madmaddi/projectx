from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^measure$', views.measure, name='measure'),
    url(r'^info$', views.info, name='info'),
    url(r'^action/(?P<action>[open|close]+)/$', views.action, name='actionWindow'),    
#url(r'^temp/(?P<id>[in|out]+)/$', views.status, name='statusTemp'),
    #url(r'^temp/(?P<id>[in|out]+)/window/(?P<action>[open|close]+)/$', views.status, name='actionWindow'),

]
