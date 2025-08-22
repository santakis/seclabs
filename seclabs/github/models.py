# -*- coding: utf-8 -*-

import os
import json
import logging
#-------------------------------------------------------------
from datetime import datetime
#/////////////////////////////////////////////////////////////
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.timezone import make_aware
#/////////////////////////////////////////////////////////////
from seclabs.github.api import Github

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
class Repository(models.Model):
    """
    The Repository model holds the information about a Github 
    Repository under the Organization. It speeds up the data 
    presentation by storing data and it updates the entries 
    by using the Github api.
    """
    repo_id = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    html_url = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    fork = models.CharField(max_length=255)
    allow_forking = models.CharField(max_length=255, default='')
    archived = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()
    pr_open = models.IntegerField(default=0)
    vulns_open = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Repository")
        verbose_name_plural = _("Repositories")

    def __str__(self):
        return self.full_name

    #/////////////////////////////////////////////////////////////
    def update(self):
        """
        The class method update is responsible to update the records 
        to map the existing organization repositories from the Github
        service and clean up any old entries.
        """
        ids = set()
        repositories = Github().get_repositories()

        for repository in repositories:
            try:
                ids.add(repository["id"])
                defaults = {
                    'repo_id': repository["id"],
                    'full_name': repository["full_name"],
                    'description': repository["description"],
                    'html_url': repository["html_url"],
                    'status': "Private" if repository["private"] == True else "Public",
                    'fork': repository["fork"],
                    'allow_forking': repository["allow_forking"],
                    'archived': repository["archived"],
                    'created_at': make_aware(datetime.strptime(repository["created_at"],"%Y-%m-%dT%H:%M:%SZ")),
                    'updated_at': make_aware(datetime.strptime(repository["updated_at"],"%Y-%m-%dT%H:%M:%SZ")),
                    'pushed_at': make_aware(datetime.strptime(repository["pushed_at"],"%Y-%m-%dT%H:%M:%SZ")),
                }
                Repository.objects.update_or_create(repo_id=repository["id"], defaults=defaults)
            except Exception as e:
                logger.error(e)

        Repository.objects.exclude(repo_id__in=ids).delete()

#/////////////////////////////////////////////////////////////
class Member(models.Model):
    """
    The Member model holds the information about the Members of 
    the Organization under Github. It speeds up the data presentation
    by storing data and it updates the entries by using the Github api.
    """
    member_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    site_admin = models.BooleanField(default=False)
    member_type = models.CharField(max_length=255)
    member_view_type = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255,blank=True,null=True)
    html_url = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.login

    #/////////////////////////////////////////////////////////////
    def update(self):
        """
        The class method update is responsible to update the records 
        to map all the existing members for the organization under the 
        Github Service and clean up any old entries.
        """
        ids = set()
        members = Github().get_members()

        for member in members:
            try:
                ids.add(member["id"])
                defaults = {
                    'member_id': member["id"],
                    'login': member["login"],
                    'site_admin': member["site_admin"],
                    'member_type': member["type"],
                    'member_view_type': member["user_view_type"],
                    'name': Github().get_user_details(member["login"]),
                    'avatar_url': member["avatar_url"],
                    'html_url': member["html_url"],
                }
                Member.objects.update_or_create(member_id=member["id"], defaults=defaults)
            except Exception as e:
                logger.error(e)

        Member.objects.exclude(member_id__in=ids).delete()

#/////////////////////////////////////////////////////////////
class Team(models.Model):
    """
    The Team model holds the information about the Teams of 
    the Organization under Github. It speeds up the data presentation
    by storing data and it updates the entries by using the Github api.
    """
    team_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    parent_team = models.CharField(max_length=255,blank=True,null=True)
    team_members = models.PositiveIntegerField(default=0)
    html_url = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name

    #/////////////////////////////////////////////////////////////
    def _safe_check_dict(self, parent):
        """
        The private class method _safe_check_dict returns a 
        dictionary value if it exists, otherwise an empty string.
        """
        if parent:
            return parent["name"]
        else:
            return "--"
 
    #/////////////////////////////////////////////////////////////
    def update(self):
        """
        The class method update is responsible to update the records 
        to map all the existing teams for the organization under the 
        Github Service and clean up any old entries.
        """
        ids = set()
        teams = Github().get_teams()

        for team in teams:
            try:
                ids.add(team["id"])
                defaults = {
                    'team_id': team["id"],
                    'name': team["name"],
                    'parent_team': self._safe_check_dict(team["parent"]),
                    'team_members': len(Github().get_team_members(team["slug"], data=[])),
                    'html_url': team["html_url"],
                }
                Team.objects.update_or_create(team_id=team["id"], defaults=defaults)
            except Exception as e:
                logger.error(e)

        Team.objects.exclude(team_id__in=ids).delete()

#/////////////////////////////////////////////////////////////
class PullRequest(models.Model):
    """
    The PullRequest model holds the information about all Github
    Pull Requests that are opened for Organization Repositories. 
    """
    pr_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    user_login = models.CharField(max_length=255)
    html_url = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)
    repo_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("PullRequest")
        verbose_name_plural = _("PullRequests")
        unique_together = ('pr_id', 'repo_id')

    def __str__(self):
        return self.pr_id

    #/////////////////////////////////////////////////////////////
    def update(self, repo_id, repo_full_name):
        """
        The class method update is responsible to update the records 
        to map the existing open pull requests for the organization 
        repositories from the Github service and clean up any old entries.
        """
        ids = set()
        pull_requests = Github().get_pull_requests(repo_full_name)
        
        for pull_request in pull_requests:
            try:
                ids.add(pull_request["id"])
                defaults = {
                    'pr_id': pull_request["id"],
                    'title': pull_request["title"],
                    'user_login': pull_request["user"]["login"],
                    'html_url': pull_request["html_url"],
                    'created_at': make_aware(datetime.strptime(pull_request["created_at"],"%Y-%m-%dT%H:%M:%SZ")),
                    'updated_at': make_aware(datetime.strptime(pull_request["updated_at"],"%Y-%m-%dT%H:%M:%SZ")),
                    'repo_id':repo_id,
                }
                PullRequest.objects.update_or_create(pr_id=pull_request["id"],repo_id=repo_id, defaults=defaults)
            except Exception as e:
                logger.error(e)
        
        PullRequest.objects.filter(repo_id=repo_id).exclude(pr_id__in=ids).delete()

#/////////////////////////////////////////////////////////////
class Dependabot(models.Model):
    """
    The Dependabot model holds the information about all Github
    Dependabot Alerts that are opened for Organization Repositories. 
    """
    vuln_id = models.CharField(max_length=255)
    package = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    state = models.CharField(max_length=255)
    severity = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    patched = models.CharField(max_length=255)
    identifiers = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)
    repo_id = models.CharField(max_length=255)
    jira_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Dependabot")
        verbose_name_plural = _("Dependabots")
        unique_together = ('vuln_id', 'repo_id')

    def __str__(self):
        return self.vuln_id
    
    #/////////////////////////////////////////////////////////////
    def update(self):
        """
        The class method update is responsible to update the records 
        to map the existing vulnerability alerts from Dependabot.
        """
        ids = set()
        dependabots = Github().get_dependabots()
        #TODO

