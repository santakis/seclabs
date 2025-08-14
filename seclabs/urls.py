# -*- coding: utf-8 -*-

#////////////////////////////////////////////////////////////
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

#////////////////////////////////////////////////////////////
import django.contrib.auth.views as auth_views

#////////////////////////////////////////////////////////////
# Application URLs
urlpatterns = [
    path('', include('seclabs.audit.urls')),
    path('', include('seclabs.users.urls')),
    path('', include('seclabs.config.urls')),
    path('', include('seclabs.jira.urls')),
    path('', include('seclabs.asana.urls')),
    path('', include('seclabs.dashboard.urls')),
]

#////////////////////////////////////////////////////////////
# Django Auth URLs
urlpatterns += [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='seclabs_login'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='seclabs_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='seclabs_logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
