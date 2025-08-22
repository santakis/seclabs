# -*- coding: utf-8 -*-

import re
import json
import logging
import requests
#/////////////////////////////////////////////////////////////
from datetime import datetime, timedelta

#/////////////////////////////////////////////////////////////
from seclabs.config.models import Config 
#-------------------------------------------------------------
from seclabs.config.utilities import get_key

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#//////////////////////////////////////////////
class Github(object):
    """
    The class Github implements the relevant HTTP API 
    calls (RESTful or Graphql) for collecting all 
    desired information from the Github service.
    """

    #//////////////////////////////////////////////
    def __init__(self):
        """
        The constructor initializes a github instance.
        """
        self.headers = dict()
        self.headers['Authorization'] = "token " + get_key("Github")
        self.headers['Accept'] = "application/vnd.github.mercy-preview+json"
        self.api = 'https://api.github.com/'
        self.org = Config().load().github_org
 
    #//////////////////////////////////////////////
    def get_repositories(self, page=1, data=[]):
        """
        The get_repositories method returns all Github repositories for the 
        Organization and their details.
        """
        url ="orgs/" + self.org + "/repos"
        opts = "?per_page=100&page=" + str(page)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)
            
            for entry in response.json():
                data.append(entry)

            if len(response.json()) == 100:
                page = page + 1
                self.get_repositories(page, data)

        except Exception as e:
            logger.critical(e)

        return data

    #//////////////////////////////////////////////
    def get_members(self, page=1, data=[]):
        """
        The get_members method returns all Github members for the 
        Organization and their details.
        """
        url ="orgs/" + self.org + "/members"
        opts = "?per_page=100&page=" + str(page)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)

            for entry in response.json():
                data.append(entry)

            if len(response.json()) == 100:
                page = page + 1
                self.get_members(page, data)

        except Exception as e:
            logger.critical(e)

        return data

    #/////////////////////////////////////////////////////////////
    def get_user_details(self, login):
        """
        The class method get_user_details returns the full name of a member 
        if it exists, otherwise gives back the login name.
        """
        url = "users/" + login

        try:
            response = requests.get(self.api + url, headers=self.headers)
            
            if response.json()["name"]:
                return response.json()["name"]
            else:
                return login

        except Exception as e:
            logger.critical(e)

    #//////////////////////////////////////////////
    def get_teams(self, page=1, data=[]):
        """
        The get_teams method returns all Github teams for the Organization 
        and their details.
        """
        url ="orgs/" + self.org + "/teams"
        opts = "?per_page=100&page=" + str(page)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)

            for entry in response.json():
                data.append(entry)

            if len(response.json()) == 100:
                page = page + 1
                self.get_members(page, data)

        except Exception as e:
            logger.critical(e)

        return data

    #/////////////////////////////////////////////////////////////
    def get_team_members(self, team, page=1, data=[]):
        """
        The class method get_team_members returns all the members 
        of a Github team.
        """
        url ="orgs/" + self.org + "/teams/" + team + "/members"
        opts = "?per_page=100&page=" + str(page)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)

            for entry in response.json():
                data.append(entry)

            if len(response.json()) == 100:
                page = page + 1
                self.get_team_members(team, page, data)

        except Exception as e:
            logger.critical(e)

        return data

    #/////////////////////////////////////////////////////////////
    def get_pull_requests(self, repo_full_name, page=1, data=[]):
        """
        The class method get_pull_requests returns all the Pull Requets
        for a repository.
        """
        url ="repos/" + repo_full_name + "/pulls"
        opts = "?per_page=100&page=" + str(page)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)

            for entry in response.json():
                data.append(entry)

            if len(response.json()) == 100:
                page = page + 1
                self.get_pull_requests(repo_full_name, page, data)

        except Exception as e:
            logger.critical(e)

        return data
 
    #/////////////////////////////////////////////////////////////
    def get_dependabots(self, page=1, data=[]):
        """
        The class method get_dependabots returns all the Dependabot Alerts
        for the Organization.
        """
        url ="orgs/" + self.org + "/dependabot/alerts"
        opts = "?per_page=100&page=" + str(page)
    
        try:
            response = requests.get(self.api + url + opts, headers=self.headers)
            logger.info(response)
            for entry in response.json():
                data.append(entry)

            if len(response.json()) == 100:
                page = page + 1
                self.get_dependabots(page, data)

        except Exception as e:
            logger.critical(e)

        return data
 
