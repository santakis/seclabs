# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.template import Library
from django.template.defaultfilters import stringfilter
#/////////////////////////////////////////////////////////////
from seclabs.jira.models import JiraUser

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
register = Library()

#/////////////////////////////////////////////////////////////
@register.filter(name='split')
@stringfilter
def split(value, delimiter):
    """
    Split value based on the given delimiter. If exception occurs return None.
    """
    try:
        return value.split(delimiter)
    except:
        return None

#/////////////////////////////////////////////////////////////
@register.filter(name='count')
def count(user_account_types, atype):
    """
    It counts the appearances of an atype (account_type) into the stored 
    list of user_account_types. If exception occurs return 0.
    """
    try:
        return user_account_types.count(atype)
    except:
        return 0

#/////////////////////////////////////////////////////////////
@register.filter(name='get_users_status')
def get_users_status(users, status):
    """
    Get Jira users filter by status value. If exception occurs return None.
    """
    try:
        return JiraUser.objects.filter(status=status)
    except:
        return None

#/////////////////////////////////////////////////////////////
@register.filter(name='get_users_account_type')
def get_users_account_type(users, account_type):
    """
    Get Jira users filter by account_type value. If exception occurs return None.
    """
    try:
        return JiraUser.objects.filter(account_type=account_type)
    except:
        return None

#/////////////////////////////////////////////////////////////
@register.filter(name='get_users_group')
def get_users_group(users, group):
    """
    Get Jira users filter by group value. If exception occurs return None.
    """
    try:
        return JiraUser.objects.filter(groups__contains=group)
    except:
        return None

#/////////////////////////////////////////////////////////////
@register.filter(name='get_users_status')
def get_users_status(users, status):
    """
    Get Jira users filter by status value. If exception occurs return None.
    """
    try:
        return JiraUser.objects.filter(status=status)
    except:
        return None


