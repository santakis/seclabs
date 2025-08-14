# -*- coding: utf-8 -*-rgs

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
from seclabs.asana.models import AsanaUser

#///////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def asana_index(request):
    """
    The main index page for Asana app within the seclabs dashboard.
    """
    log_request(request)

    users = AsanaUser.objects.all()

    response = {
        "users":users.count(),
        "admins":users.filter(is_admin=True).count(),
        "guests":users.filter(is_guest=True).count(),
        "active":users.filter(status="Active").count(),
    }

    return render(request, 'asana/dashboard/asana-index.html', response)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def asana_users(request):
    """
    The Asana users view within the seclabs dashboard.
    """
    log_request(request)
    
    query = filters = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
     
        match request.GET['q']:
            case "is_admin":
                filters = Q(is_admin=True)
            case "is_guest":
                filters = Q(is_guest=True)
            case "is_view_only":
                filters = Q(is_view_only=True)
                
        users = AsanaUser.objects.filter(
            Q(gid__icontains=query)|
            Q(full_name__icontains=query)|
            Q(email__icontains=query)|
            Q(status__icontains=query)
        ).order_by("-is_admin")
        
        if filters:
            users = AsanaUser.objects.filter(filters)

    if not query or (query and not users):
        users = AsanaUser.objects.order_by("-is_admin")
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
    return render(request, 'asana/dashboard/asana-users.html', response)

