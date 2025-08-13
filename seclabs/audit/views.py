# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
#-------------------------------------------------------------
from django.core.paginator import Paginator, InvalidPage
from django.core.paginator import EmptyPage, PageNotAnInteger
#-------------------------------------------------------------
from seclabs.audit.logger import log_request
#-------------------------------------------------------------
from seclabs.users.decorators import superuser_required
#-------------------------------------------------------------
from seclabs.audit.models import AuditLogs

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def index(request):
    """
    The view audit_index shows the auditing logs of Users that 
    accessed seclabs platform.
    """
    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        auditlogs = AuditLogs.objects.filter(
                Q(first_name__icontains=query)|
                Q(last_name__icontains=query)|
                Q(username__icontains=query)|
                Q(request_path__icontains=query)|
                Q(method__icontains=query)
            ).order_by("-timestamp")
        search = True

    if not query or (query and not auditlogs):
        auditlogs = AuditLogs.objects.order_by("-timestamp")
        search = False

    paginator = Paginator(auditlogs, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        auditlogs = paginator.page(page)
    except InvalidPage:
        auditlogs = paginator.page(int(1))
    except PageNotAnInteger:
        auditlogs = paginator.page(int(1))
    except EmptyPage:
        auditlogs = paginator.page(int(1))

    response = {
        'auditlogs':auditlogs,
        'query':query,
        'search':search,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'audit/dashboard/audit-index.html', response)

