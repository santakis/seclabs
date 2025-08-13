# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.conf import settings
#-------------------------------------------------------------
from seclabs.config.aes import decrypt
#-------------------------------------------------------------
from seclabs.config.models import AccessKey

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
def get_key(service, account=False):
    """
    The get_key method returns the decrypted Access Key based on 
    the idientifier, if the service does not exist, then it 
    returns nothing.
    """
    try:    
        accesskeyIs = AccessKey.objects.get(service=service)

        if account:
            return accesskeyIs.account, decrypt(accesskeyIs.key) 
        
        return decrypt(accesskeyIs.key)
    except AccessKey.DoesNotExist:    
        logger.error("AccessKey for service" + str(service) + " not found!")
        return None

