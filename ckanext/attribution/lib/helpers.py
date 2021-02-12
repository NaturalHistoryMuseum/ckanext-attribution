#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools

from ckan.plugins import toolkit
from ckanext.attribution.model.crud import PackageContributionActivityQuery


def can_edit():
    '''
    Check editing permissions for updating agent directly.
    :return:
    '''
    try:
        permitted = toolkit.check_access(u'agent_update', {}, {})
        return permitted
    except toolkit.NotAuthorized:
        return False


def get_agents(pkg_id):
    '''

    :param pkg_id:
    :return:
    '''
    link_records = PackageContributionActivityQuery.read_package(pkg_id)
    activities = sorted([r.contribution_activity for r in link_records], key=lambda x: x.activity)
    grouped_activities = {
        k: [a.agent for a in sorted(v, key=lambda x: len(list(v)) if x.order is None else x.order)] for
        k, v in itertools.groupby(activities, key=lambda x: x.activity)}
    return grouped_activities
