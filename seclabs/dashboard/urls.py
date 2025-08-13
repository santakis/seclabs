# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.dashboard import views as dashboard_views

#////////////////////////////////////////////////////////////
# Dashboard URLs
urlpatterns = [
    path('dashboard/index/', dashboard_views.index, name='dashboard_index'),
    path('robots.txt', dashboard_views.robot, name='dashboard_robots'),
]

