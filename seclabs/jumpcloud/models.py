# -*- coding: utf-8 -*-

import re
import logging
#-------------------------------------------------------------
from datetime import datetime
#/////////////////////////////////////////////////////////////
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.timezone import make_aware
#/////////////////////////////////////////////////////////////
from seclabs.jumpcloud.api import JumpCloud

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
class JumpCloudUser(models.Model):
    """
    The JumpCloudUser model holds specific information 
    for JumpCloud users.
    """
    gid = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    #--
    devices = models.TextField(blank=True,null=True)
    no_devices = models.IntegerField(default=0)
    #--
    employee_type = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    #--
    locked = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)
    suspended = models.BooleanField(default=False)
    state = models.CharField(max_length=255)
    #--
    sudo = models.BooleanField(default=False)
    pass_date = models.DateTimeField()
    pass_expired = models.BooleanField(default=False)
    totp = models.BooleanField(default=False)
    mfa = models.CharField(max_length=255)
    #--
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("JumpCloudUser")
        verbose_name_plural = _("JumpCloudUser")

    def __str__(self):
        return self.full_name

    #//////////////////////////////////////////
    def _safe_check(self, dictionary, key):
        """
        The _safe_check method returns a dictionary value
        if it exists, otherwise an empty string.
        """
        try:
            data = dictionary[key]
        except:
            data = ""
    
        return data

    #/////////////////////////////////////////////////////////////
    def update(self):
        """ 
        The class method update is responsible to update the records
        for JumpCloud users and their status.
        """
        users = JumpCloud().get_users()
        ids = set()

        for user in users:

            try:
                ids.add(user["id"])
                devices, number = JumpCloud().get_user_devices(user["id"])

                defaults = {
                    "gid": user["id"],
                    "full_name": user["displayname"],
                    "email": user["email"],
                    "username": user["username"],
                    "devices": devices,
                    "no_devices": number,
                    "employee_type": user["employeeType"],
                    "job_title": self._safe_check(user, "jobTitle"),
                    "location": user["location"],
                    "department": user["department"],
                    "locked": user["account_locked"],
                    "activated": user["activated"],
                    "suspended": user["suspended"],
                    "state": user["state"],
                    "sudo": user["sudo"],
                    "pass_date": make_aware(datetime.strptime(user["password_date"],"%Y-%m-%dT%H:%M:%S.%fZ")),
                    "pass_expired": user["password_expired"],
                    "totp": user["totp_enabled"],
                    "mfa": user["mfaEnrollment"]["overallStatus"],
                    "created": make_aware(datetime.strptime(user["created"],"%Y-%m-%dT%H:%M:%S.%fZ")),
                }
                JumpCloudUser.objects.update_or_create(gid=user["id"], defaults=defaults)
            except Exception as e:
                logger.error(e)

        JumpCloudUser.objects.exclude(gid__in=ids).delete()

