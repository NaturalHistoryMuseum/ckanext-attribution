#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import DomainObject, meta, user_table
from ckan.model.types import make_uuid
from sqlalchemy import (Boolean, Column, ForeignKey, Table, UnicodeText)

# this table stores agent
agent_table = Table(
    u'agent',
    meta.metadata,
    Column(u'id', UnicodeText, primary_key=True, default=make_uuid),
    Column(u'agent_type', UnicodeText, nullable=False),
    Column(u'family_name', UnicodeText, nullable=True),
    Column(u'given_names', UnicodeText, nullable=True),
    Column(u'given_names_first', Boolean, nullable=False, default=True),
    Column(u'name', UnicodeText, nullable=True),
    Column(u'orcid', UnicodeText, nullable=True, unique=True),
    Column(u'ror_id', UnicodeText, nullable=True, unique=True),
    Column(u'user_id', UnicodeText,
           ForeignKey(u'user.id', onupdate=u'CASCADE', ondelete=u'CASCADE'), nullable=True)
)


class Agent(DomainObject):
    '''An agent (e.g. a researcher or institution) that contributes to a package.'''

    @property
    def affiliations(self):
        return {a.other_agent(self.id): a for a in self._affiliations}


def check_for_table():
    ''' '''
    if user_table.exists():
        agent_table.create(checkfirst=True)
