# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.conf import settings
#-------------------------------------------------------------
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

#/////////////////////////////////////////////////////////////
from seclabs.users.forms import EditUserForm

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
def edit_user(request, id):
    """
    The method edit_user performs the editing of a User 
    instance by loading and saving the relevant User form 
    instance.
    """
    try:
        user = User.objects.get(id=id)
        form = EditUserForm(initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'title': user.profile.title,
            'company': user.profile.company,
            'location': user.profile.location,
            'timezone': user.profile.timezone,
        }, id=id)
        return form
    except User.DoesNotExist:    
        logger.error("User ID: " + str(id) + " not found!")
        return None
 
#/////////////////////////////////////////////////////////////
def update_user(id,fn,ln,un,em,ti,co,lo,tz,st,su,ac):
    """
    The method update_user retrieves the User instance 
    and saves all given changes to the database.
    """
    try:
        user = User.objects.get(id=id)
        user.first_name = fn
        user.last_name = ln
        user.username = un
        user.email = em
        #-----------------------
        user.is_staff = st
        user.is_superuser = su
        user.is_active = ac
        #-----------------------
        user.profile.title = ti
        user.profile.company = co
        user.profile.location = lo
        user.profile.timezone = tz
        user.save()
    except User.DoesNotExist:
        logger.error("User ID: " + str(id) + " update failed!")

#/////////////////////////////////////////////////////////////
def create_user(fn,ln,un,em,ti,co,p1,lo,tz,st,su,ac):
    """
    The method create_user creates a new User instance 
    with the given data and saves it to the database.
    """
    try:
        user = User()
        user.first_name = fn
        user.last_name = ln
        user.username = un
        user.email = em
        user.password = make_password(p1)
        user.is_staff = st
        user.is_superuser = su
        user.is_active = ac
        user.save()
        #-----------------------
        user.profile.title = ti
        user.profile.company = co
        user.profile.location = lo
        user.profile.timezone = tz
        user.save()
    except Exception as e:
       logger.warning("User creation failed!")
       logger.error(e)

#/////////////////////////////////////////////////////////////
def update_password(id,p1):
    """
    The method update_password changes a User instance 
    password and saves it to the database.
    """
    try:
        user = User.objects.get(id=id)
        user.password = make_password(p1)
        user.save()
    except User.DoesNotExist:
        logger.error("User ID: " + str(id) + " update failed!")

