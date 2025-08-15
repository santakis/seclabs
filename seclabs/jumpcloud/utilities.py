# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////
from seclabs.jumpcloud.models import JumpCloudUser

#/////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#//////////////////////////////////////////////
def jumpcloud_update_data():
    """
    The method jumpcloud_update_data is updating all models 
    under jumpcloud app with latest available data.
    """
    JumpCloudUser().update()

