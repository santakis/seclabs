# -*- coding: utf-8 -*-rgs


import logging
#///////////////////////////////////////////////////////////////
from django.db.models import Q
from django.http import Http404
from django.conf import settings
from django.shortcuts import render, redirect
#---------------------------------------------------------------
from django.core.paginator import Paginator, InvalidPage
from django.core.paginator import EmptyPage, PageNotAnInteger
#---------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
#---------------------------------------------------------------
from seclabs.users.logger import log_request

#///////////////////////////////////////////////////////////////
from seclabs.config.forms import ConfigForm
#---------------------------------------------------------------
from seclabs.config.actions import edit_config
from seclabs.config.actions import update_config
#---------------------------------------------------------------
from seclabs.config.models import AccessKey
from seclabs.config.forms import AccessKeyForm
#---------------------------------------------------------------
from seclabs.config.actions import edit_accesskey
from seclabs.config.actions import create_accesskey
from seclabs.config.actions import update_accesskey
#---------------------------------------------------------------
from seclabs.users.helpers import cascade_models
from seclabs.users.decorators import superuser_required

#///////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
def config_index(request):
    """
    The view config_index updates the organization level
    configuration options.
    """
 
    log_request(request)
    
    form = edit_config(request)
    
    if not form :    
        logger.critical("Could not retrieve Configuration form.")
        raise Http404

    if request.method == 'POST':

        form = ConfigForm(request.POST)

        if form.is_valid():
            update_config(
                form.cleaned_data['jira_server'],
                form.cleaned_data['github_org'])

            return redirect('dashboard_index')
 
    return render(request,'config/dashboard/config-index.html', {'form':form,})

#///////////////////////////////////////////////////////////////
@never_cache
@login_required
def accesskeys_index(request):
    """
    The view accesskeys_index shows the list of existing AccessKeys
    inside the platform.
    """
    log_request(request)

    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        accesskeys = AccessKey.objects.filter(
                Q(account__icontains=query)|
                Q(service__icontains=query)
            ).order_by("-created")
        search = True

    if not query or (query and not accesskeys):
        accesskeys = AccessKey.objects.order_by("-created")
        search = False

    paginator = Paginator(accesskeys, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        accesskeys = paginator.page(page)
    except InvalidPage:
        accesskeys = paginator.page(int(1))
    except PageNotAnInteger:
        accesskeys = paginator.page(int(1))
    except EmptyPage:
        accesskeys = paginator.page(int(1))

    response = {
        'accesskeys':accesskeys,
        'query':query,
        'search':search,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'config/dashboard/accesskeys-index.html', response)

#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def accesskeys_create(request):
    """
    The view accesskeys_create implements the creation of a New AccessKey
    inside the platform. The privilege of AccessKey creation is only given
    to the 'Superuser Role'.
    """
    log_request(request)

    form = AccessKeyForm(id=None)

    if request.method == 'POST': 
        
        form = AccessKeyForm(request.POST, id=None)
        
        if form.is_valid(): 
            
            ac = form.cleaned_data['account']
            ke = form.cleaned_data['key']
            se = form.cleaned_data['service']
            
            create_accesskey(ac,ke,se)

            return redirect('dashboard_accesskeys')
    
    return render(request, 'config/dashboard/accesskey-create.html', { 'form':form, })

#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def accesskeys_edit(request, id):
    """
    The view accesskeys_edit allows changes of an existing AccessKey instance
    inside the platform. The privilege of AccessKey editing is only given
    to the 'Superuser Role'.
    """
    log_request(request)
    
    try:
        accesskeyIs = AccessKey.objects.get(id=id)   
    except AccessKey.DoesNotExist:
        logger.critical("AccessKey ID was not found: " + str(id))
        raise Http404

    form = edit_accesskey(request, id)

    if not form :    
        logger.critical("Could not retrieve form, based on AccessKey ID :" + str(id))
        raise Http404

    if request.method == 'POST':

        form = AccessKeyForm(request.POST, id=id)

        if form.is_valid():
            
            update_accesskey(id,
                form.cleaned_data['account'],
                form.cleaned_data['key'],
                form.cleaned_data['service'])

            return redirect('dashboard_accesskeys')
  
    response = {
        'form':form,
        'accesskeyIs':accesskeyIs,
    }
    return render(request,'config/dashboard/accesskey-edit.html', response)

#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def accesskeys_delete(request, id):
    """
    The accesskeys_delete view allows the deletion of a AccessKey instance. The 
    view asks for confirmation and presents any db-relations with other models. 
    The privilege of deleting a AccessKey instance is only given to the 'Superuser Role'.
    """
    log_request(request)

    try:
        accesskeyIs = AccessKey.objects.get(id=id)   
        response = {
            'items':cascade_models(accesskeyIs),
            'accesskeyIs':accesskeyIs,
        }
        return render(request, 'config/dashboard/accesskey-delete.html', response)
    except AccessKey.DoesNotExist:
        logger.critical("AccessKey ID was not found: " + str(id))
        raise Http404
    
#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def accesskeys_erase(request, id):
    """
    The accesskeys_erase view performs the final actions for deletion.
    """
    log_request(request)

    try:
        accesskeyIs = AccessKey.objects.get(id=id)   
        accesskeyIs.delete()
        return redirect('dashboard_accesskeys')
    except AccessKey.DoesNotExist:
        logger.critical("AccessKey ID was not found: " + str(id))
        raise Http404

