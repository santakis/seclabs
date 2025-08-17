# -*- coding: utf-8 -*-

import json
import logging
#-------------------------------------------------------------
import requests
from requests.auth import HTTPBasicAuth
#/////////////////////////////////////////////////////////////
from django.conf import settings
#-------------------------------------------------------------
from datetime import datetime, timedelta

#/////////////////////////////////////////////////////////////
from seclabs.config.models import Config
#-------------------------------------------------------------
from seclabs.config.utilities import get_key

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#//////////////////////////////////////////////
class Jira:
    """
    The class Jira implements the relevant HTTP API 
    calls (RESTful) for collecting all desired information 
    from the Jira service.
    """

    #//////////////////////////////////////////////
    def __init__(self):
        """
        The constructor initializes a jira instance.
        """
        self.headers = dict()
        self.headers['Accept'] = "application/json"
        #---
        account, token = get_key("Jira", True)
        self.auth = HTTPBasicAuth(account, token)
        #---
        self.api = Config.load().jira_server + "/rest/api/2/"

    #//////////////////////////////////////////////
    def get_users(self, offset=0, data=[]):
        """
        The get_users method returns all Jira users and their details 
        after performing all relevant calls.
        """
        url ="/users/search"
        opts = "?maxResults=1000&startAt=" + str(offset)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers, auth=self.auth)

            for entry in response.json():
                data.append(entry)
            
            if len(response.json()) == 1000:
                offset = offset + 1000
                self.get_users(offset, data)

        except Exception as e:
            logger.critical(e)

        return data

    #//////////////////////////////////////////////
    def get_user_groups(self, account_id):
        """
        The get_user_groups method returns the groups assigned to a specific 
        Jira user (account_id).
        """
        groups = list()

        url = "user/groups?accountId=" + str(account_id)
        opts = "&maxResults=1000"
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers, auth=self.auth)
           
            for entry in response.json():
                groups.append(entry["name"])

        except Exception as e:
            logger.critical(e)

        if not groups:
            return "", 0

        return ",".join(groups), len(groups)

    #//////////////////////////////////////////////
    def get_groups(self, offset=0, data=[]):
        """
        The get_groups method returns all Jira groups and their details 
        after performing all relevant calls.
        """
        url ="group/bulk"
        opts = "?maxResults=50&startAt=" + str(offset)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers, auth=self.auth)
            
            for entry in response.json()["values"]:
                data.append(entry)

            if len(response.json()["values"]) == 50:
                offset = offset + 50
                self.get_groups(offset, data)

        except Exception as e:
            logger.critical(e)

        return data

    #//////////////////////////////////////////////
    def get_group_users(self, group_id):
        """
        The get_group_users method returns the users assigned to a specific 
        Jira group (group_id).
        """
        users = list()

        url = "group/member/?groupId=" + str(group_id)
        opts = "&maxResults=50"
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers, auth=self.auth)
 
            for entry in response.json()["values"]:
                users.append(entry)

        except Exception as e:
            logger.critical(e)

        if not users:
            return "", 0

        return users, len(users)

