# -*- coding: utf-8 -*-

import logging
#/////////////////////////////////////////////////////////////////
from django.db.models.deletion import Collector

#/////////////////////////////////////////////////////////////////
logger = logging.getLogger(__name__)

#/////////////////////////////////////////////////////////////////
def cascade_models(item):
    items = list()
    try:
        collector = Collector(using='default')
        collector.collect([item])
        for model, instance in collector.instances_with_model():
            items.append((model._meta.verbose_name, instance))
    except Exception as e:
        logger.info(e)
        logger.error("Error, failed to get related models.")

    return items

