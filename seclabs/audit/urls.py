# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.urls import path, re_path
#------------------------------------------------------------
from seclabs.audit import views as audit_views

#////////////////////////////////////////////////////////////
# Logs URLs
urlpatterns = [
    path('dashboard/audit/', audit_views.index, name='dashboard_audit')
]

