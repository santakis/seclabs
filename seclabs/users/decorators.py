# -*- coding: utf-8 -*-

#/////////////////////////////////////////////////////////////
from django.contrib.auth.decorators import user_passes_test

#/////////////////////////////////////////////////////////////
def superuser_required(view_func=None):

    actual_decorator = user_passes_test(
            lambda u: u.is_superuser, 
            login_url='dashboard_index', 
            redirect_field_name=None
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

