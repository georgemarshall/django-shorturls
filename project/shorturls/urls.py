from django.conf.urls import patterns, include, url

from .views import ShortURLView

urlpatterns = patterns('',
    url(r'^(?P<token>[\w\-_]+)$', ShortURLView.as_view(), name='index'),
    # url(r'^(?P<token>[\w\-_]+)/stats/$', ShortURLStatsView.as_view(), name='stats'),
)
