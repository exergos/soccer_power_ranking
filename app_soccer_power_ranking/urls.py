from django.conf.urls import patterns, url
from app_soccer_power_ranking import views

urlpatterns = patterns('',
        url(r'^ranking/$', views.ranking, name='ranking'),
        url(r'^chart/$', views.chart, name='chart'))