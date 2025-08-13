# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.jira import views as jira_views

#////////////////////////////////////////////////////////////
# Jira URLs
urlpatterns = [
    path('dashboard/jira/', jira_views.jira_index, name='dashboard_jira'),
    path('dashboard/jira/users/', jira_views.jira_users, name='dashboard_jira_users'),
    path('dashboard/jira/groups/', jira_views.jira_groups, name='dashboard_jira_groups'),
]
