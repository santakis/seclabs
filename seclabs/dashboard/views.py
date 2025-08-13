# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
#-------------------------------------------------------------
from seclabs.audit.logger import log_request
#-------------------------------------------------------------
#from seclabs.users.decorators import superuser_required

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def index(request):
    """
    The main dashboard page.
    """
    log_request(request)

    response = {}
    return render(request, 'dashboard/dashboard-index.html', response)

#/////////////////////////////////////////////////////////////
def robot(request,):
    """
    The robot view is returning the robots.txt file.
    """
    log_request(request)
    
    try:
        robot_file = open(os.path.join(settings.TEMPLATES_DIR, 'robots.txt'), 'rb')
        robots = robot_file.read()
    except:
        raise Http404

    return HttpResponse(robots, content_type='text/plain')
