# -*- coding: utf-8 -*-

from django import forms
#///////////////////////////////////////////////////////////////
from django.utils.translation import gettext as _

#///////////////////////////////////////////////////////////////
w_first_name = forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'id':'users-first_name', 'type':'text', 'autocomplete':'off', 'placeholder':_('John')})
w_last_name = forms.TextInput(attrs={'class':'form-control', 'tabindex':'2', 'id':'users-last_name', 'type':'text', 'autocomplete':'off', 'placeholder':_('Wick')})
w_username = forms.TextInput(attrs={'class':'form-control', 'tabindex':'3', 'id':'users-username', 'type':'text', 'autocomplete':'off', 'placeholder':_('john.wick')})
w_email = forms.EmailInput(attrs={'class':'form-control', 'tabindex':'4', 'id':'users-email', 'type':'text', 'autocomplete':'off', 'placeholder':_('john.wick@continental.cc')})
w_title = forms.TextInput(attrs={'class':'form-control', 'tabindex':'5', 'id':'users-title', 'type':'text', 'autocomplete':'off', 'placeholder':_('Retired Hitman')})
w_company = forms.TextInput(attrs={'class':'form-control', 'tabindex':'6', 'id':'users-company', 'type':'text', 'autocomplete':'off', 'placeholder':_('Freelancer')})
w_password1 = forms.PasswordInput(attrs={'class':'form-control', 'tabindex':'7', 'id':'users-password1', 'type':'password', 'autocomplete':'off', 'placeholder':_('Enter Password')})
w_password2 = forms.PasswordInput(render_value=True,attrs={'class':'form-control', 'tabindex':'8', 'id':'users-password2', 'type':'password', 'autocomplete':'off', 'placeholder':_('Confirm Password')})
w_location = forms.TextInput(attrs={'class':'form-control', 'tabindex':'9', 'id':'users-location', 'type':'text', 'autocomplete':'off', 'placeholder':_('New York')})
w_timezone = forms.TextInput(attrs={'class':'form-control', 'tabindex':'10', 'id':'users-timezone', 'type':'text', 'autocomplete':'off', 'placeholder':_('GMT-4')})
w_is_active = forms.CheckboxInput(attrs={'class':'form-check-input', 'tabindex':'10', 'id':'users-is_active', 'type':'checkbox'})
w_is_superuser = forms.CheckboxInput(attrs={'class':'form-check-input', 'tabindex':'11', 'id':'users-is_superuser', 'type':'checkbox'})
w_is_staff = forms.CheckboxInput(attrs={'class':'form-check-input', 'tabindex':'12', 'id':'users-is_staff', 'type':'checkbox'})

#///////////////////////////////////////////////////////////////
e_password_confirmation = _("You must confirm your password.")
e_password_match = _("Your passwords do not match.")
e_username_exists = _("This username is already being used.")
e_email_exists = _("This email is already being used.")

