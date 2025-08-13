# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.db import models
from django.utils.translation import gettext as _

#/////////////////////////////////////////////////////////////
class AuditLogs(models.Model):
    """
    The AuditLogs class is responsible for storing actions 
    performed by all Users accessing the seclabs platform.

    """
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=False)
    is_superuser = models.BooleanField()
    #-----------
    ipaddress = models.CharField(max_length=255, blank=True)
    request_path = models.CharField(max_length=255, blank=False)
    method = models.CharField(max_length=5, blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Audit Logs")
        verbose_name_plural = _("Audit Logs")

    def __str__(self):
        return self.timestamp

