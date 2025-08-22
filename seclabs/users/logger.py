# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////////
from seclabs.users.models import AuditLog

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
            auditlog = AuditLog()
            auditlog.first_name = request.user.first_name
            auditlog.last_name = request.user.last_name
            auditlog.is_superuser = request.user.is_superuser
            auditlog.username = request.user

            if request.META['REMOTE_ADDR']:
                auditlog.ipaddress = request.META['REMOTE_ADDR']

            auditlog.request_path = request.path
            auditlog.method = request.META['REQUEST_METHOD']
            auditlog.save()
    except Exception as e:
        logger.error(e)

