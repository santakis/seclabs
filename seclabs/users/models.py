# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext as _
#-------------------------------------------------------------
from django.dispatch import receiver
#/////////////////////////////////////////////////////////////
from django.contrib.auth.models import User 

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
class Profile(models.Model):
    """
    The Profile class extends the default ``User`` model for storing
    additional information fo the user. The association is OneToOneField, 
    and signals are used for syncing the objects.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _("User's Profile")
        verbose_name_plural = _("User's Profile")

    def __str__(self):
        return self.user.username

    #/////////////////////////////////////////////////////////////
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """
        The create_user_profile method is executed on the post_save
        signal for every newly created User object.
        """
        if created:
            Profile.objects.create(user=instance)

    #/////////////////////////////////////////////////////////////
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """
        The save_user_profile method is executed on the post_save
        signal for every User object.
        """
        instance.profile.save()

#/////////////////////////////////////////////////////////////
class AuditLog(models.Model):
    """
    The AuditLog class is responsible for storing actions 
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

