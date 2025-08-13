# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////////
from seclabs.audit.models import AuditLogs 

#/////////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////////
def log_request(request):
    """
    The log_request method it records data coming from the HTTP-request,
    such as: username, ip-address, http-method, request-path. This is 
    done for auditing access to the platform.
    """
    try:
        if request.user.is_authenticated:
            auditlogs = AuditLogs()
            auditlogs.first_name = request.user.first_name
            auditlogs.last_name = request.user.last_name
            auditlogs.is_superuser = request.user.is_superuser
            auditlogs.username = request.user

            if request.META['REMOTE_ADDR']:
                auditlogs.ipaddress = request.META['REMOTE_ADDR']

            auditlogs.request_path = request.path
            auditlogs.method = request.META['REQUEST_METHOD']
            auditlogs.save()
    except Exception as e:
        logger.error(e)

