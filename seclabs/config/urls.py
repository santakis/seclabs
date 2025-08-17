# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.config import views as config_views

#////////////////////////////////////////////////////////////
# Users URLs
urlpatterns = [
    path('dashboard/config/index', config_views.config_index, name='dashboard_config'),
    path('dashboard/accesskeys/', config_views.accesskeys_index, name='dashboard_accesskeys'),
    path('dashboard/accesskeys/create/', config_views.accesskeys_create, name='dashboard_accesskeys_create'),
    re_path(r'^dashboard/accesskeys/edit/(?P<id>\d+)/$', config_views.accesskeys_edit, name='dashboard_accesskeys_edit'),
    re_path(r'^dashboard/accesskeys/delete/(?P<id>\d+)/$', config_views.accesskeys_delete, name='dashboard_accesskeys_delete'),
    re_path(r'^dashboard/accesskeys/erase/(?P<id>\d+)/$', config_views.accesskeys_erase, name='dashboard_accesskeys_erase'),
]

