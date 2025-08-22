#i -*- coding: utf-8 -*-rgs

import os
import logging
#///////////////////////////////////////////////////////////////
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponse
#---------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
#---------------------------------------------------------------
from django.core.paginator import Paginator, InvalidPage
from django.core.paginator import EmptyPage, PageNotAnInteger
#---------------------------------------------------------------
from seclabs.users.logger import log_request
#---------------------------------------------------------------
from seclabs.users.decorators import superuser_required
#///////////////////////////////////////////////////////////////
from collections import OrderedDict
#-------------------------------------------------------------
from seclabs.github.models import Repository
from seclabs.github.models import Member
from seclabs.github.models import Team
from seclabs.github.models import PullRequest
from seclabs.github.models import Dependabot

#///////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def github_index(request):
    """
    The index page for Github data
    """
    log_request(request)
    return render(request, 'github/dashboard/github-index.html')

#///////////////////////////////////////////////////////////////
@never_cache
@login_required
def github_repos(request):
    """
    The view github_repos presents the existing Github repositories
    under organization structure.
    """
    log_request(request)

    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
        
        repos = Repository.objects.filter(
            Q(repo_id__icontains=query)|
            Q(full_name__icontains=query)|
            Q(status__icontains=query)|
            Q(fork__icontains=query)
        ).order_by("-vulns_open", "-pr_open")
    
    if not query or (query and not repos):
        repos = Repository.objects.order_by("-vulns_open", "-pr_open")
        search = False
 
    paginator = Paginator(repos, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        repos = paginator.page(page)
    except InvalidPage:
        repos = paginator.page(int(1))
    except PageNotAnInteger:
        repos = paginator.page(int(1))
    except EmptyPage:
        repos = paginator.page(int(1))

    response = {
        'query':query,
        'search':search,
        'repos':repos,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'github/dashboard/github-repos.html', response)

#///////////////////////////////////////////////////////////////
@never_cache
@login_required
def github_members(request):
    """
    The view member presents all the members under the Organization
    and their details. 
    """
    log_request(request)
 
    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
        
        members = Member.objects.filter(
            Q(member_id__icontains=query)|
            Q(name__icontains=query)|
            Q(contributions__icontains=query)|
            Q(login__icontains=query)
        ).order_by("site_admin")
    
    if not query or (query and not members):
        members = Member.objects.order_by("site_admin")
        search = False
 
    paginator = Paginator(members, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        members = paginator.page(page)
    except InvalidPage:
        members = paginator.page(int(1))
    except PageNotAnInteger:
        members = paginator.page(int(1))
    except EmptyPage:
        members = paginator.page(int(1))

    response = {
        'query':query,
        'search':search,
        'members':members,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'github/dashboard/github-members.html', response)

#///////////////////////////////////////////////////////////////
@never_cache
@login_required
def github_teams(request):
    """
    The view team presents all the teams under the Organization
    and their details. 
    """
    log_request(request)
 
    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
        
        teams = Team.objects.filter(
            Q(team_id__icontains=query)|
            Q(name__icontains=query)|
            Q(parent_team__icontains=query)
        ).order_by("-team_members")
    
    if not query or (query and not teams):
        teams = Team.objects.order_by("-team_members")
        search = False
 
    paginator = Paginator(teams, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        teams = paginator.page(page)
    except InvalidPage:
        teams = paginator.page(int(1))
    except PageNotAnInteger:
        teams = paginator.page(int(1))
    except EmptyPage:
        teams = paginator.page(int(1))

    response = {
        'query':query,
        'search':search,
        'teams':teams,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'github/dashboard/github-teams.html', response)

#///////////////////////////////////////////////////////////////
@never_cache
@login_required
def github_dependabots(request):
    """
    The view github_dependabots presents the existing dependabot 
    alerts for the Organization.
    """
    log_request(request)

    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
        
        dependabots = Dependabot.objects.filter(
            Q(vuln_id__icontains=query)|
            Q(package__icontains=query)|
            Q(state__icontains=query)|
            Q(severity__icontains=query)|
            Q(patched__icontains=query)|
            Q(identifiers__icontains=query)|
            Q(repo_id__icontains=query)|
            Q(jira_id__icontains=query)
        ).order_by("-created_at", "state")
    
    if not query or (query and not dependabots):
        dependabots = Dependabot.objects.order_by("-created_at", "state")
        search = False
 
    paginator = Paginator(dependabots, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        dependabots = paginator.page(page)
    except InvalidPage:
        dependabots = paginator.page(int(1))
    except PageNotAnInteger:
        dependabots = paginator.page(int(1))
    except EmptyPage:
        dependabots = paginator.page(int(1))

    response = {
        'query':query,
        'search':search,
        'dependabots':dependabots,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'github/dashboard/github-dependabots.html', response)

#///////////////////////////////////////////////////////////////
@never_cache
@login_required
def github_repo_pull_requests(request, repo_id):
    """
    The view github_repo_pull_requests presents the existing
    Github pull_requests under organization repositories.
    """
    log_request(request)

    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
        
        pull_requests = PullRequest.objects.filter(repo_id=repo_id).filter(
            Q(pr_id__icontains=query)|
            Q(title__icontains=query)|
            Q(user_login__icontains=query)
        ).order_by("-created_at")
    
    if not query or (query and not pull_requests):
        pull_requests = PullRequest.objects.filter(repo_id=repo_id).order_by("-created_at")
        search = False
 
    paginator = Paginator(pull_requests, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        pull_requests = paginator.page(page)
    except InvalidPage:
        pull_requests = paginator.page(int(1))
    except PageNotAnInteger:
        pull_requests = paginator.page(int(1))
    except EmptyPage:
        pull_requests = paginator.page(int(1))

    response = {
        'query':query,
        'search':search,
        'repository':Repository.objects.get(repo_id=repo_id),
        'pull_requests':pull_requests,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'github/dashboard/github-repo-pull-requests.html', response)


