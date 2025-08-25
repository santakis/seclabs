# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.db.models import Sum
from django.conf import settings
from django.template import Library
from django.template.defaultfilters import stringfilter
#-------------------------------------------------------------
from seclabs.github.models import Repository
#-------------------------------------------------------------
from seclabs.config.models import Config 

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
register = Library()

#/////////////////////////////////////////////////////////////////
@register.filter(name='get_repo_name')
def get_repo_name(value):
    """
    Get the repo name from an id. If exception occurs, return empty string.
    """
    try:
        full_name = Repository.objects.get(repo_id=value).full_name
        return full_name.rsplit("/", 1)[-1]
    except:
        return ""

