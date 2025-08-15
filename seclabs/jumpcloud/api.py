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
class JumpCloud:
    """
    The class JumpCloud implements the relevant HTTP API calls 
    for collecting all desired information from the JumpCloud platform.
    """

    #//////////////////////////////////////////////
    def __init__(self):
        """
        The constructor initializes a asana instance.
        """
        self.headers = dict()
        self.headers['x-api-key'] = get_key("JumpCloud", False)
        self.headers['Accept'] = "application/json"
        self.api = "https://console.jumpcloud.com/api/"
 
    #//////////////////////////////////////////////
    def get_users(self, offset=0, data=[]):
        """
        The get_users method returns all JumpCloud users and their details 
        after performing all relevant calls.
        """
        url ="systemusers"
        opts = "?limit=100&sort=lastname&skip=" + str(offset)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)

            for entry in response.json()["results"]:
                data.append(entry)
            
            if len(response.json()["results"]) == 100:
                offset = offset + 100
                self.get_users(offset, data)

        except Exception as e:
            logger.critical(e)

        return data

    #//////////////////////////////////////////////
    def get_user_devices(self, user_id):
        """
        The get_user_devices method returns a deviced assigned to a specific 
        JumpCloud user_id.
        """
        devices = list()

        url ="v2/users/" + str(user_id) + "/systems"
        opts = "?details=v1&skip=0&limit=100"
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)
           
            for entry in response.json():
                devices.append(entry["hostname"])

        except Exception as e:
            logger.critical(e)

        if not devices:
            return "", 0

        return ",".join(devices), len(devices)

    #//////////////////////////////////////////////
    def get_devices(self, offset=0, data=[]):
        """
        The get_devices method returns all JumpCloud devices and their details 
        after performing all relevant calls.
        """
        url ="systems"
        opts = "?limit=100&sort=displayName&skip=" + str(offset)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)

            for entry in response.json()["results"]:
                data.append(entry)
            
            if len(response.json()["results"]) == 100:
                offset = offset + 100
                self.get_devices(offset, data)

        except Exception as e:
            logger.critical(e)

        return data

