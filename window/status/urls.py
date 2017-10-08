from django.conf.urls import url

from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),

    #url(r'^info$', views.info, name='info'),

    url(r'^environment$', views.tempList, name='temp'),
    url(r'^environment/measure$', views.measure, name='measure'),
    url(r'^environment/(?P<key>[0-9]+)$', views.tempDetail, name='temp'),

    url(r'^window$', views.windowState, name='windowStatus'),
    url(r'^window/(?P<action>[open|close]+)$', views.action, name='actionWindow'),

    ###
    #url(r'^snippets/$', views.snippet_list),
    #url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),

]

urlpatterns = format_suffix_patterns(urlpatterns)