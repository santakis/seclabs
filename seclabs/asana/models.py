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
from seclabs.asana.api import Asana

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
class AsanaUser(models.Model):
    """
    The AsanaUser model holds specific information from Asana users.
    """
    gid = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    #--
    status = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    is_view_only = models.BooleanField(default=False)
    #--
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("AsanaUser")
        verbose_name_plural = _("AsanaUser")

    def __str__(self):
        return self.full_name

    #/////////////////////////////////////////////////////////////
    def update(self):
        """ 
        The class method update is responsible to update the records
        for Asana users and their status.
        """
        users = Asana().get_users()
        ids = set()

        for user in users["data"]:

            status = Asana().get_user_status(user["gid"])["data"][0]

            try:
                ids.add(user["gid"])
                defaults = { 
                    "gid": user["gid"],
                    "full_name": user["name"],
                    "email": user["email"],
                    "status": "Active" if status["is_active"] == True else "Disabled",
                    "is_admin": status["is_admin"],
                    "is_guest": status["is_guest"],
                    "is_view_only": status["is_view_only"],
                    "created": make_aware(datetime.strptime(status["created_at"],"%Y-%m-%dT%H:%M:%S.%fZ")),
                }
                AsanaUser.objects.update_or_create(gid=user["gid"], defaults=defaults)
            except Exception as e:
                logger.error(e)

        AsanaUser.objects.exclude(gid__in=ids).delete()

