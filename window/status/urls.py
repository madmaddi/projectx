from django.conf.urls import url

from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^measure$', views.measure, name='measure'),

    url(r'^info$', views.info, name='info'),

    url(r'^temp/$', views.tempList, name='temp'),
    url(r'^temp/(?P<key>[0-9]+)/$', views.tempDetail, name='temp'),

    url(r'^window/$', views.windowState, name='windowStatus'),
    url(r'^window/(?P<action>[open|close]+)/$', views.action, name='actionWindow'),

    ###
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
#url(r'^temp/(?P<id>[in|out]+)/$', views.status, name='statusTemp'),
    #url(r'^temp/(?P<id>[in|out]+)/window/(?P<action>[open|close]+)/$', views.status, name='actionWindow'),

]

urlpatterns = format_suffix_patterns(urlpatterns)