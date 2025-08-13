# -*- coding: utf-8 -*-

#///////////////////////////////////////////////////////////////
from django import forms
from django.contrib.auth.password_validation import validate_password
#---------------------------------------------------------------
from seclabs.users.widgets import *
#---------------------------------------------------------------

#///////////////////////////////////////////////////////////////
from django.contrib.auth.models import User

#///////////////////////////////////////////////////////////////
class CreateUserForm(forms.Form):

    use_required_attribute = False

    first_name = forms.CharField(max_length=150, min_length=3, widget=w_first_name)
    last_name = forms.CharField(max_length=150, min_length=3, widget=w_last_name)
    username = forms.CharField(max_length=150, min_length=3, widget=w_username)
    email = forms.EmailField(widget=w_email)
    password1 = forms.CharField(max_length=30, widget=w_password1, validators=[validate_password])
    password2 = forms.CharField(max_length=30, widget=w_password2, validators=[validate_password])

    title = forms.CharField(max_length=100, widget=w_title)
    company = forms.CharField(max_length=100, widget=w_company)
    location = forms.CharField(max_length=100, widget=w_location)
    timezone = forms.CharField(max_length=100, widget=w_timezone)
    
    is_staff = forms.BooleanField(required=False, widget=w_is_staff)
    is_superuser = forms.BooleanField(required=False, widget=w_is_superuser)
    is_active = forms.BooleanField(required=False, widget=w_is_active)

    #////////////////////////////////
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError(e_password_confirmation)
        if password1 != password2:
            raise forms.ValidationError(e_password_match)

        return password2

    #////////////////////////////////
    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            userIs = User.objects.get(username=username)
            raise forms.ValidationError(e_username_exists)
        except User.DoesNotExist:
            return username

    #////////////////////////////////
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            userIs = User.objects.get(email=email)
            raise forms.ValidationError(e_email_exists)
        except User.DoesNotExist:
            return email

#///////////////////////////////////////////////////////////////
class EditUserForm(forms.Form):

    #///////////////////////////////////////////////
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id')
        super(EditUserForm, self).__init__(*args, **kwargs)

    use_required_attribute = False

    first_name = forms.CharField(max_length=150, min_length=3, widget=w_first_name)
    last_name = forms.CharField(max_length=150, min_length=3, widget=w_last_name)
    username = forms.CharField(max_length=150, min_length=3, widget=w_username)
    email = forms.EmailField(widget=w_email)

    title = forms.CharField(max_length=100, widget=w_title)
    company = forms.CharField(max_length=100, widget=w_company)
    location = forms.CharField(max_length=100, widget=w_location)
    timezone = forms.CharField(max_length=100, widget=w_timezone)

    is_staff = forms.BooleanField(required=False, widget=w_is_staff)
    is_superuser = forms.BooleanField(required=False, widget=w_is_superuser)
    is_active = forms.BooleanField(required=False, widget=w_is_active)

    #////////////////////////////////
    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            userIs = User.objects.get(username=username)
            if str(userIs.id) == self.id:
                return username
            raise forms.ValidationError(e_username_exists)
        except User.DoesNotExist:
            return username

    #////////////////////////////////
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            userIs = User.objects.get(email=email)
            if str(userIs.id) == self.id:
                return email
            raise forms.ValidationError(e_email_exists)
        except User.DoesNotExist:
            return email

#///////////////////////////////////////////////////////////////
class UserPasswordForm(forms.Form):

    use_required_attribute = False

    password1 = forms.CharField(max_length=30, widget=w_password1, validators=[validate_password])
    password2 = forms.CharField(max_length=30, widget=w_password2, validators=[validate_password])

    #////////////////////////////////
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError(e_password_confirmation)
        if password1 != password2:
            raise forms.ValidationError(e_password_match)

        return password2

