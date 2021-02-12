#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import DomainObject, meta
from ckan.model.types import make_uuid
from ckanext.attribution.model.agent import agent_table
from ckanext.attribution.model.contribution_activity import (contribution_activity_table)
from sqlalchemy import (Column, ForeignKey, Table, UnicodeText)

agent_contribution_activity_table = Table(
    u'agent_contribution_activity',
    meta.metadata,
    Column(u'id', UnicodeText, primary_key=True, default=make_uuid),
    Column(u'agent_id', UnicodeText,
           ForeignKey(u'agent.id', onupdate=u'CASCADE', ondelete=u'CASCADE'), nullable=False),
    Column(u'contribution_activity_id', UnicodeText,
           ForeignKey(u'contribution_activity.id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
           nullable=False, unique=True),
)


class AgentContributionActivity(DomainObject):
    '''A link between an agent and the contribution activity performed.'''
    pass


def check_for_table():
    ''' '''
    if agent_table.exists() and contribution_activity_table.exists():
        agent_contribution_activity_table.create(checkfirst=True)
