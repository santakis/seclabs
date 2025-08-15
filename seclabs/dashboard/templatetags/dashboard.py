# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.template import Library
from django.template.defaultfilters import stringfilter

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

