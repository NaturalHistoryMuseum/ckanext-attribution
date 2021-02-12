#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckanext.attribution.model.agent_affiliation import (AgentAffiliation,
                                                         agent_affiliation_table)

from ._base import BaseQuery


class AgentAffiliationQuery(BaseQuery):
    ''' '''
    # model and table (subclasses should override)
    m = AgentAffiliation
    t = agent_affiliation_table
