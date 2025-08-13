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
from seclabs.config.utilities import get_key
from seclabs.jira.api import Jira

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
class JiraUser(models.Model):
    """
    The JiraUser model holds specific information from Jira users
    which are relevant to security processes such as Off-Boarding,
    On-Boarding.
    """
    account_id = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)  
    avatar_url = models.CharField(max_length=255) 
    account_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    groups = models.TextField(blank=True,null=True)
    no_groups = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("JiraUser")
        verbose_name_plural = _("JiraUser")

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
        The class method update is responsible for retrieving the latest 
        information with regards to specific Jira Users.
        """
        users = Jira().get_users()
        ids = set()

        for user in users:
            try:
                ids.add(user["accountId"])
                groups, number = Jira().get_user_groups(user["accountId"])

                defaults = {
                    'account_id': user["accountId"],
                    'full_name': user["displayName"],
                    'email': self._safe_check(user, "emailAddress"),
                    'avatar_url': user["avatarUrls"]["24x24"],
                    'account_type': user["accountType"],
                    'status': "Active" if user["active"] == True else "Disabled",
                    'groups': groups,
                    'no_groups': number,
                }
                JiraUser.objects.update_or_create(account_id=user["accountId"], defaults=defaults)
            except Exception as e:
                logger.error(e)

        JiraUser.objects.exclude(account_id__in=ids).delete()

#/////////////////////////////////////////////////////////////
class JiraGroup(models.Model):
    """
    The JiraGroup model holds specific information from Jira groups
    and the user members of each group.
    """
    group_id = models.CharField(max_length=255, unique=True)
    group_name = models.CharField(max_length=255)
    user_names = models.TextField(blank=True,null=True)
    user_emails = models.TextField(blank=True,null=True)
    user_account_types = models.TextField(blank=True,null=True)
    no_users = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("JiraGroup")
        verbose_name_plural = _("JiraGroup")

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
        The class method update is responsible for retrieving the latest 
        information with regards to specific Jira Users.
        """
        groups = Jira().get_groups()
        ids = set()
        
        for group in groups:
            try:
                ids.add(group["groupId"])
                users, number = Jira().get_group_users(group["groupId"])
                
                user_names = list()
                user_emails = list()
                user_account_types = list()

                for user in users:
                    user_names.append(user["displayName"])
                    user_emails.append(self._safe_check(user, "emailAddress"))
                    user_account_types.append(user["accountType"])
                
                defaults = {
                    'group_id': group["groupId"],
                    'group_name': group["name"],
                    'user_names': ",".join(user_names),
                    'user_emails': ",".join(user_emails),
                    'user_account_types': ",".join(user_account_types),
                    'no_users': number,
                }
                JiraGroup.objects.update_or_create(group_id=group["groupId"], defaults=defaults)
            except Exception as e:
                logger.error(e)

        JiraGroup.objects.exclude(group_id__in=ids).delete()

