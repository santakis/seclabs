# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.asana import views as asana_views

#////////////////////////////////////////////////////////////
# Asana URLs
urlpatterns = [
    path('dashboard/asana/', asana_views.asana_index, name='dashboard_asana'),
    path('dashboard/asana/users/', asana_views.asana_users, name='dashboard_asana_users'),
]
