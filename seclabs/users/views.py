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
from django.contrib.auth.models import User
#---------------------------------------------------------------
from seclabs.users.forms import CreateUserForm
from seclabs.users.forms import EditUserForm
from seclabs.users.forms import UserPasswordForm
#---------------------------------------------------------------
from seclabs.users.actions import edit_user
from seclabs.users.actions import create_user
from seclabs.users.actions import update_user
from seclabs.users.actions import update_password
#---------------------------------------------------------------
from seclabs.users.models import AuditLog
#---------------------------------------------------------------
from seclabs.users.helpers import cascade_models
from seclabs.users.decorators import superuser_required

#///////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
def users_index(request):
    """
    The main index page for Users app within the seclabs dashboard.
    """
    log_request(request)

    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        users = User.objects.filter(
                Q(first_name__icontains=query)|
                Q(last_name__icontains=query)|
                Q(username__icontains=query)|
                Q(email__icontains=query)
            ).order_by("is_superuser")
        search = True

    if not query or (query and not users):
        users = User.objects.order_by("is_superuser")
        search = False

    paginator = Paginator(users, settings.PAGES)
    page = request.GET.get('page', 1)

    try:
        users = paginator.page(page)
    except InvalidPage:
        users = paginator.page(int(1))
    except PageNotAnInteger:
        users = paginator.page(int(1))
    except EmptyPage:
        users = paginator.page(int(1))

    response = {
        'users':users,
        'query':query,
        'search':search,
        'total':paginator.count,
        'pages':paginator.num_pages,
        'page_range':range(1,paginator.num_pages+1),
    }
    return render(request, 'users/dashboard/users-index.html', response)

#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def users_create(request):
    """
    The view users_create implements the creation of a New User
    inside the platform. The privilege of User creation is only given
    to the 'Superuser Role'.
    """
    log_request(request)

    form = CreateUserForm()

    if request.method == 'POST': 
        
        form = CreateUserForm(request.POST)
        
        if form.is_valid(): 
            
            fn = form.cleaned_data['first_name']
            ln = form.cleaned_data['last_name']
            un = form.cleaned_data['username']
            em = form.cleaned_data['email']
            p1 = form.cleaned_data['password1']
            p2 = form.cleaned_data['password2']
            #-------------------------
            ti = form.cleaned_data['title']
            co = form.cleaned_data['company']
            lo = form.cleaned_data['location']
            tz = form.cleaned_data['timezone']
            #-------------------------
            st = form.cleaned_data['is_staff']
            su = form.cleaned_data['is_superuser']
            ac = form.cleaned_data['is_active']
            
            create_user(fn,ln,un,em,ti,co,p1,lo,tz,st,su,ac)

            return redirect('dashboard_users')
    
    return render(request, 'users/dashboard/user-create.html', { 'form':form, })

#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def users_edit(request, id):
    """
    The view users_edit allows changes of an existing User instance
    inside the platform. The privilege of User editing is only given
    to the 'Superuser Role'.
    """
    log_request(request)
    
    try:
        userIs = User.objects.get(id=id)   
    except User.DoesNotExist:
        logger.critical("User ID was not found: " + str(idm))
        raise Http404

    form = edit_user(request, id)

    if not form :    
        logger.critical("Could not retrieve form, based on User ID :" + str(id))
        raise Http404

    if request.method == 'POST':

        form = EditUserForm(request.POST, id=id)

        if form.is_valid():
            
            update_user(id,
                form.cleaned_data['first_name'],
                form.cleaned_data['last_name'],
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['title'],
                form.cleaned_data['company'],
                form.cleaned_data['location'],
                form.cleaned_data['timezone'],
                form.cleaned_data['is_staff'],
                form.cleaned_data['is_superuser'],
                form.cleaned_data['is_active'])

            return redirect('dashboard_users')
  
    response = {
        'form':form,
        'userIs':userIs,
    }
    return render(request,'users/dashboard/user-edit.html', response)

#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def users_password(request, id):
    """
    The users_password view provides the ability to reset a User's password.
    The privilege of changing a User Password is only given to the 'Superuser Role'.
    """
    log_request(request)
    
    try:
        userIs = User.objects.get(id=id)   
    except User.DoesNotExist:
        logger.critical("User ID was not found: " + str(id))
        raise Http404

    p_form = UserPasswordForm()

    if request.method == 'POST':

        p_form = UserPasswordForm(request.POST)

        if p_form.is_valid():
            update_password(id, p_form.cleaned_data['password1'])
            return redirect('dashboard_users')

    response = {
        'p_form':p_form,
        'userIs':userIs,
    }
    return render(request,'users/dashboard/user-password.html', response)
    
#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def users_delete(request, id):
    """
    The users_delete view allows the deletion of a User instance. The 
    view asks for confirmation and presents any db-relations with other 
    models. The privilege of deleting a User instance is only given to the 
    'Superuser Role'.
    """
    log_request(request)

    try:
        userIs = User.objects.get(id=id)   
        response = {
            'items':cascade_models(userIs),
            'userIs':userIs,
        }
        return render(request, 'users/dashboard/user-delete.html', response)
    except User.DoesNotExist:
        logger.critical("User ID was not found: " + str(id))
        raise Http404
    
#/////////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def users_erase(request, id):
    """
    The users_erase view performs the final actions for deletion.
    """
    log_request(request)

    try:
        userIs = User.objects.get(id=id)   
        userIs.delete()
        return redirect('dashboard_users')
    except User.DoesNotExist:
        logger.critical("User ID was not found: " + str(id))
        raise Http404

#/////////////////////////////////////////////////////////////
@never_cache
@login_required
@superuser_required
def users_audit(request):
    """
    The view users_audit shows the auditing logs of Users that 
    accessed seclabs platform.
    """
    query = ''

    if request.GET and 'q' in request.GET:
        query = " ".join(request.GET['q'].split())
        auditlogs = AuditLog.objects.filter(
                Q(first_name__icontains=query)|
                Q(last_name__icontains=query)|
                Q(username__icontains=query)|
                Q(request_path__icontains=query)|
                Q(method__icontains=query)
            ).order_by("-timestamp")
        search = True

    if not query or (query and not auditlogs):
        auditlogs = AuditLog.objects.order_by("-timestamp")
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
    return render(request, 'users/dashboard/users-audit.html', response)

