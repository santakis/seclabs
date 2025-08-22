# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.conf import settings
#////////////////////////////////////////////////////////////
from seclabs.config.models import Config

#////////////////////////////////////////////////////////////
# Context processor for SITE_URL
def site_url(request):
    """
    The site_url method is a contenxt processor for ``SITE_URL``. 
    The variable is defined under settings.py and it becomes 
    avalaible to all project templates.
    """
    return {'SITE_URL': settings.SITE_URL}

#////////////////////////////////////////////////////////////
# Context processor for SITE_DATE
def site_date(request):
    """
    The site_date method is a contenxt processor for ``SITE_DATE``. 
    The variable, which is defined under settings.py and it becomes 
    avalaible to all project templates.
    """
    return {'SITE_DATE': settings.SITE_DATE}

#////////////////////////////////////////////////////////////
# Context processor for SITE_DOCS
def site_docs(request):
    """
    The site_docs method is a contenxt processor for SITE_DOCS.
    The variable is defined under settings.py and it becomes 
    avalaible to all project templates.
    """
    return {'SITE_DOCS': settings.SITE_DOCS}

#////////////////////////////////////////////////////////////
# Context processor for GITHUB_ORG
def github_org(request):
    """
    The github_org method is a contenxt processor for GITHUB_ORG.
    The variable is defined under Config model by the user and it 
    becomes avalaible to all project templates.
    """
    return {'GITHUB_ORG': Config().load().github_org}

