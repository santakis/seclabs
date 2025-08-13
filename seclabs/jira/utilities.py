# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from seclabs.jira.models import JiraUser
from seclabs.jira.models import JiraGroup

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#//////////////////////////////////////////////
def jira_update_data():
    """
    The method jira_update_data is updating all models under jira app
    with latest available data.
    """
    JiraUser().update()
    JiraGroup().update()

