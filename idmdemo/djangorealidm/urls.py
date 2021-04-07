from django.urls import re_path

from . import views

urlpatterns = [
        re_path(r'^approve/(?P<grant_id>\d+)/(?P<next_state_id>\d+)/$', views.approve_ticket, name='approve'),
    ]
