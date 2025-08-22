# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.users import views as users_views

#////////////////////////////////////////////////////////////
# Users URLs
urlpatterns = [
    path('dashboard/users/', users_views.users_index, name='dashboard_users'),
    path('dashboard/users/audit/', users_views.users_audit, name='dashboard_users_audit'),
    path('dashboard/users/create/', users_views.users_create, name='dashboard_users_create'),
    re_path(r'^dashboard/users/edit/(?P<id>\d+)/$', users_views.users_edit, name='dashboard_users_edit'),
    re_path(r'^dashboard/users/password/(?P<id>\d+)/$', users_views.users_password, name='dashboard_users_password'),
    re_path(r'^dashboard/users/delete/(?P<id>\d+)/$', users_views.users_delete, name='dashboard_users_delete'),
    re_path(r'^dashboard/users/erase/(?P<id>\d+)/$', users_views.users_erase, name='dashboard_users_erase'),
]

