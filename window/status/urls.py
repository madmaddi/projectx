from django.conf.urls import url

from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^environment$', views.environmentList, name='temp'),
    url(r'^environment/measure$', views.measure, name='measure'),
    url(r'^environment/(?P<key>[0-9]+)$', views.environmentDetail, name='temp'),

    url(r'^window$', views.windowState, name='windowStatus'),
    url(r'^window/(?P<action>[open|close]+)$', views.action, name='actionWindow'),

]

urlpatterns = format_suffix_patterns(urlpatterns)