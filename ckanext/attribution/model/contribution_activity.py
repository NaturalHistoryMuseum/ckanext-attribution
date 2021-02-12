#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import DomainObject, meta
from ckan.model.types import make_uuid
from sqlalchemy import (Column, DateTime, Table, UnicodeText, Integer)

# this table stores contribution activities
contribution_activity_table = Table(
    u'contribution_activity',
    meta.metadata,
    Column(u'id', UnicodeText, primary_key=True, default=make_uuid),
    Column(u'activity', UnicodeText, nullable=False),
    Column(u'level', UnicodeText, nullable=True),
    Column(u'time', DateTime, nullable=True),
    Column(u'order', Integer, nullable=True)
)


class ContributionActivity(DomainObject):
    '''A contribution activity record.'''
    pass


def check_for_table():
    ''' '''
    contribution_activity_table.create(checkfirst=True)
