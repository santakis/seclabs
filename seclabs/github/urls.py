# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.github import views as github_views

#////////////////////////////////////////////////////////////
# Github URLs
urlpatterns = [
    path('dashboard/github/index/', github_views.github_index, name='dashboard_github'),
    path('dashboard/github/repos/', github_views.github_repos, name='dashboard_github_repos'),
    path('dashboard/github/members/', github_views.github_members, name='dashboard_github_members'),
    path('dashboard/github/teams/', github_views.github_teams, name='dashboard_github_teams'),
    path('dashboard/github/dependabots/', github_views.github_dependabots, name='dashboard_github_dependabots'),
    re_path(r'^dashboard/github/repo-pull-requests/(?P<repo_id>[0-9]+)/$', github_views.github_repo_pull_requests, name='dashboard_github_repo_pull_requests'),
]
