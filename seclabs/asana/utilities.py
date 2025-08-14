# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from seclabs.asana.models import AsanaUser

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#//////////////////////////////////////////////
def asana_update_data():
    """
    The method asana_update_data is updating all models under asana app
    with latest available data.
    """
    AsanaUser().update()

