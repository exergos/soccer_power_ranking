from django.conf.urls import patterns, url
from app_soccer_power_ranking import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))