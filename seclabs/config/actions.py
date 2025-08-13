# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.conf import settings
#/////////////////////////////////////////////////////////////
from seclabs.config.models import AccessKey
from seclabs.config.forms import AccessKeyForm

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
def edit_accesskey(request, id):
    """
    The method edit_accesskey performs the editing of an Access Key
    instance by loading and saving the AccessKey form instance.
    """
    try:
        accesskey = AccessKey.objects.get(id=id)
        form = AccessKeyForm(initial = {
            'account': accesskey.account,
            'service': accesskey.service,
        }, id=id)
        return form
    except AccessKey.DoesNotExist:    
        logger.error("AccessKey ID: " + str(id) + " not found!")
        return None
 
#/////////////////////////////////////////////////////////////
def update_accesskey(id,ac,ke,se):
    """
    The method update_accesskey retrieves the AccessKey instance 
    and saves all given changes to the database.
    """
    try:
        accesskey = AccessKey.objects.get(id=id)
        accesskey.account = ac
        accesskey.key = ke
        accesskey.service = se
        accesskey.save()
    except AccessKey.DoesNotExist:
        logger.error("AccessKey ID: " + str(id) + " update failed!")

#/////////////////////////////////////////////////////////////
def create_accesskey(ac,ke,se):
    """
    The method create_accesskey creates a new AccessKey instance 
    with the given data and saves it to the database.
    """
    try:
        accesskey = AccessKey()
        accesskey.account = ac
        accesskey.key = ke
        accesskey.service = se
        accesskey.save()
    except Exception as e:
       logger.warning("AccessKey creation failed!")
       logger.error(e)

