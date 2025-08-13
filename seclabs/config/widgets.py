# -*- coding: utf-8 -*-

from django import forms
#///////////////////////////////////////////////////////////////
from django.utils.translation import gettext as _

#///////////////////////////////////////////////////////////////
w_account = forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'id':'config-account', 'type':'text', 'autocomplete':'off', 'placeholder':_('secops@seclabs.com')})
w_key = forms.TextInput(attrs={'class':'form-control', 'tabindex':'2', 'id':'config-key', 'type':'text', 'autocomplete':'off', 'placeholder':_('Enter secret, api-key, token')})
w_service = forms.Select(attrs={'class':'form-control', 'tabindex':'3', 'id':'config-service'})

#///////////////////////////////////////////////////////////////
e_service_exists = _("There is already a key for that service.")

