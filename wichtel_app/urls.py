# from django.urls import path


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.event_list, name='index'),
    url(r'^events/?$', views.event_list, name='event_list'),
    url(r'^events/(?P<id>[0-9]+)/?$', views.event_detail, name='event_detail'),
    url(r'^events/(?P<id>[0-9]+)/complete/?$', views.event_complete, name='event_complete'),
    url(r'^events/(?P<id>[0-9]+)/clear/?$', views.event_clear, name='event_clear'),
    url(r'^events/new/?$', views.event_new, name='event_new'),
    url(r'^users/(?P<id>[0-9]+)/?$', views.participant_detail, name='participant_detail'),
    url(r'^impressum$', views.impressum, name='impressum'),
    url(r'^privacy$', views.privacy, name='privacy'),
]
