#-*- coding: utf-8 -*-

#///////////////////////////////////////////////////////////////
from django import forms
#---------------------------------------------------------------
from seclabs.config.widgets import *
#---------------------------------------------------------------

#///////////////////////////////////////////////////////////////
from seclabs.config.models import AccessKey, SERVICES

#/////////////////////////////////////////////////////////////////
class ConfigForm(forms.Form):

    use_required_attribute = False
 
    jira_server = forms.CharField(max_length=256, widget=w_jira_server)
    github_org = forms.CharField(max_length=256, widget=w_github_org)

#///////////////////////////////////////////////////////////////
class AccessKeyForm(forms.Form):

    #///////////////////////////////////////////////
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id')
        super(AccessKeyForm, self).__init__(*args, **kwargs)

    use_required_attribute = False

    account = forms.CharField(max_length=255, widget=w_account)
    key = forms.CharField(max_length=255, widget=w_key)
    service = forms.ChoiceField(choices=SERVICES, widget=w_service)
 
    #////////////////////////////////
    def clean_service(self):
        service = self.cleaned_data.get('service')

        try:
            accesskeyIs = AccessKey.objects.get(service=service)
            if str(accesskeyIs.id) == self.id:
                return service
            raise forms.ValidationError(e_service_exists)
        except AccessKey.DoesNotExist:
            return service

