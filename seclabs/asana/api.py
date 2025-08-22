# -*- coding: utf-8 -*-

import json
import logging
import requests
#/////////////////////////////////////////////////////////////
from django.utils.translation import gettext as _
#/////////////////////////////////////////////////////////////
from seclabs.config.utilities import get_key

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#//////////////////////////////////////////////
class Asana:
    """
    The class Asana implements the relevant HTTP API calls
    for collecting all desired information from the Asana platform.
    """

    #//////////////////////////////////////////////
    def __init__(self):
        """
        The constructor initializes a asana instance.
        """
        self.headers = dict()
        self.headers['Authorization'] = get_key("Asana")
        self.headers['Accept'] = "application/json"
        self.api = "https://app.asana.com/api/1.0/"
 
    #//////////////////////////////////////////////
    def get_user_status(self, gid):
        """
        The get_user_status method returns specific useful information for the
        user status.
        """
        url = "users/" + str(gid) + "/workspace_memberships"
        opts = "?opt_fields=created_at,is_admin,is_view_only,is_guest,is_active"
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)
            return response.json()
        except Exception as e:
            logger.critical(e)

    #//////////////////////////////////////////////
    def get_users(self):
        """
        The get_users method returns all Asana users and their details 
        after performing all relevant calls.
        """
        url = "workspaces/149651404743580/users?opt_fields=name,email"

        try:
            response = requests.get(self.api + url, headers=self.headers)
            return response.json()
        except Exception as e:
            logger.critical(e)

