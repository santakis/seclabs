#i -*- coding: utf-8 -*-rgs

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
from seclabs.audit.logger import log_request

#///////////////////////////////////////////////////////////////
from seclabs.jira.models import JiraUser
from seclabs.jira.models import JiraGroup

#///////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def jira_index(request):
    """
    The main index page for Jira app within the seclabs dashboard.
    """
    log_request(request)

    users = JiraUser.objects.all()

    response = {
        "users":users,
        "groups":JiraGroup.objects.all().count(),
    }

    return render(request, 'jira/dashboard/jira-index.html', response)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def jira_users(request):
    """
    The Jira users view within the seclabs dashboard.
    """
    log_request(request)
    
    query = filters = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
     
        if 'strict' in request.GET:
             match request.GET['strict']:
                case "fullname":
                    filters = Q(full_name__icontains=query)
                case "email":
                    filters = Q(email__icontains=query)
                case "atype":
                    filters = Q(account_type__icontains=query)
                case "status":
                    filters = Q(status__icontains=query)
                case "groups":
                    filters = Q(groups__icontains=query)
                
        users = JiraUser.objects.filter(
            Q(account_id__icontains=query)|
            Q(full_name__icontains=query)|
            Q(email__icontains=query)|
            Q(account_type__icontains=query)|
            Q(status__icontains=query)|
            Q(groups__icontains=query)
        ).order_by("status")
        
        if filters:
            users = JiraUser.objects.filter(filters)

    if not query or (query and not users):
        users = JiraUser.objects.order_by("status")
        search = False
 
    paginator = Paginator(users, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        users = paginator.page(page)
    except InvalidPage:
        users = paginator.page(int(1))
    except PageNotAnInteger:
        esers = paginator.page(int(1))
    except EmptyPage:
        users = paginator.page(int(1))

    response = {
        'query':query,
        'search':search,
        'users':users,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'jira/dashboard/jira-users.html', response)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def jira_groups(request):
    """
    The Jira groups view within the seclabs dashboard.
    """
    log_request(request)
    
    query = filters = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
     
        if 'strict' in request.GET:
             match request.GET['strict']:
                case "name":
                    filters = Q(group_name__icontains=query)
                case "email":
                    filters = Q(user_emails__icontains=query)
                case "user":
                    filters = Q(user_names__icontains=query)
                
        groups = JiraGroup.objects.filter(
            Q(group_id=query)|
            Q(group_name__icontains=query)|
            Q(user_names__icontains=query)|
            Q(user_emails__icontains=query)
        ).order_by("group_name")
        
        if filters:
            groups = JiraUser.objects.filter(filters)

    if not query or (query and not groups):
        groups = JiraGroup.objects.order_by("group_name")
        search = False
 
    paginator = Paginator(groups, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        groups = paginator.page(page)
    except InvalidPage:
        groups = paginator.page(int(1))
    except PageNotAnInteger:
        esers = paginator.page(int(1))
    except EmptyPage:
        groups = paginator.page(int(1))

    response = {
        'query':query,
        'search':search,
        'groups':groups,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'jira/dashboard/jira-groups.html', response)

