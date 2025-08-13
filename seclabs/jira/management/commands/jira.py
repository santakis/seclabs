# -*- coding: utf-8 -*-

import logging
#////////////////////////////////////////////////////////////////////////
from django.core.management.base import BaseCommand
#------------------------------------------------------------------------
from seclabs.jira.utilities import jira_update_data

#/////////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#////////////////////////////////////////////////////////////////////////
class Command(BaseCommand):
    """
    A method that is used for exposing a command-line interface for the application
    that can be used for running manually tasks.
    """
    #/////////////////////////////////////////////
    def add_arguments(self, parser):
        """
            A list of command line arguments:
                * python3 manage.py jira --update (Update Jira data)
        """
        parser.add_argument('--update', action='store_true', dest='update', default=False, help='Update Jira data.')
                                            
    #/////////////////////////////////////////////
    def handle(self, *args, **options):

        if options['update']:
            logger.info("jira-management: Update infomration.")
            jira_update_data()

