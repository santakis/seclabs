# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.jumpcloud import views as jumpcloud_views

#////////////////////////////////////////////////////////////
# JumpCloud URLs
urlpatterns = [
    path('dashboard/jumpcloud/', jumpcloud_views.jumpcloud_index, name='dashboard_jumpcloud'),
    path('dashboard/jumpcloud/users/', jumpcloud_views.jumpcloud_users, name='dashboard_jumpcloud_users'),
    path('dashboard/jumpcloud/devices/', jumpcloud_views.jumpcloud_devices, name='dashboard_jumpcloud_devices'),
]
