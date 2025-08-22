# -*- coding: utf-8 -*-

import os
import logging
from datetime import timedelta
#/////////////////////////////////////////////////////////////
from django.conf import settings
from django.utils import timezone
#/////////////////////////////////////////////////////////////
from seclabs.github.models import Repository
from seclabs.github.models import Member
from seclabs.github.models import Team
from seclabs.github.models import PullRequest
from seclabs.github.models import Dependabot

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#//////////////////////////////////////////////
def github_update_data():
    """
    The method github_update_data is re-querying and updating all 
    Github data stored inside the models. 
    """
    repo_objs = list()

    #Repository().update()
    #Member().update()
    #Team().update()
    Dependabot().update()

    #for repository in Repository.objects.filter(archived="False"):
        #PullRequest().update(repository.repo_id, repository.full_name)
        #repository.pr_open = PullRequest.objects.filter(repo_id=repository.repo_id).count()
        #repository.vulns_open = Dependabot.objects.filter(state="open").filter(repo_id=repository.repo_id).count()
        #repo_objs.append(repository)

    #for repository in Repository.objects.filter(archived="True"):
        #PullRequest.objects.filter(repo_id=repository.repo_id).delete()
        #Dependabot.objects.filter(repo_id=repository.repo_id).delete()
        #repository.pr_open = 0
        #repository.vulns_open = 0
        #repo_objs.append(repository)
    
    #Repository.objects.bulk_update(repo_objs, ['pr_open', 'vulns_open'], batch_size=500)
    #Repository.objects.bulk_update(repo_objs, ['pr_open',], batch_size=500)

