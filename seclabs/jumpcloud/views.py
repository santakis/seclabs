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
from seclabs.jumpcloud.models import JumpCloudUser

#///////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def jumpcloud_index(request):
    """
    The main index page for JumpCloud app within the seclabs dashboard.
    """
    log_request(request)
    return render(request, 'jumpcloud/dashboard/jumpcloud-index.html')

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def jumpcloud_users(request):
    """
    The JumpCloud users view within the seclabs dashboard.
    """
    log_request(request)
    
    query = filters = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        search = True
     
        users = JumpCloudUser.objects.filter(
            Q(gid__icontains=query)|
            Q(full_name__icontains=query)|
            Q(email__icontains=query)|
            Q(username__icontains=query)|
            Q(devices__icontains=query) |
            Q(employee_type__icontains=query)|
            Q(job_title__icontains=query)|
            Q(location__icontains=query)|
            Q(department__icontains=query)|
            Q(state__icontains=query)|
            Q(mfa__icontains=query)
        ).order_by("created")
        
    if not query or (query and not users):
        users = JumpCloudUser.objects.order_by("created")
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
    return render(request, 'jumpcloud/dashboard/jumpcloud-users.html', response)


