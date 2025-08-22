# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from django.db.models import Sum
from django.conf import settings
from django.template import Library
from django.template.defaultfilters import stringfilter
#-------------------------------------------------------------
from seclabs.github.models import Repository
from seclabs.github.models import Member
from seclabs.github.models import PullRequest
from seclabs.github.models import Dependabot
#-------------------------------------------------------------
from seclabs.config.models import Config 

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////
register = Library()

#/////////////////////////////////////////////////////////////////
# placeholder
