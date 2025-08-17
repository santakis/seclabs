# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
#-------------------------------------------------------------
from seclabs.config.aes import encrypt

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
SERVICES = (
    ('Jira', _('Jira')),
    ('Asana', _('Asana')),
    ('Github', _('Github')),
    ('JumpCloud', _('JumpCloud')),
    ('Cisco Umbrella', _('Cisco Umbrella')),
)

#/////////////////////////////////////////////////////////////////
class SingletonModel(models.Model):
    """
    The SingletonModel class is a one instance db-modeling abstraction
    for holding information such as configuration options.
    """

    class Meta:
        abstract = True

    #///////////////////////////////
    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    #///////////////////////////////
    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

#/////////////////////////////////////////////////////////////////
class Config(SingletonModel):
    """
    The Config class holds organization level configuration options.
    """
    jira_server = models.CharField(max_length=255, null=True, blank=True)
    github_org = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Config')
        verbose_name_plural = _('Configs')

#/////////////////////////////////////////////////////////////
class AccessKey(models.Model):
    """
    The AccessKey class holds the relevant API-Keys or Access 
    Tokens for accessing externa services. The information is 
    encrypted and it appears under seclabs configuation view
    """
    
    account = models.CharField(max_length=255, default='')
    key = models.BinaryField(max_length=500, default=b'')
    service = models.CharField(max_length=25, choices=SERVICES, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Access Key")
        verbose_name_plural = _("Access Keys")

    def __str__(self):
        return "%s (%s)" % (self.account, self.service)

#/////////////////////////////////////////////////////////////
@receiver(pre_save, sender=AccessKey)
def encrypt_key(sender, instance, **kwargs):
    """
    The encrypt_key method is executed on the pre_save
    signal for every Access Key object.
    """
    instance.key= encrypt(instance.key)

