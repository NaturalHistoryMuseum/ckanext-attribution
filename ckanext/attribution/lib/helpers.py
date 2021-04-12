#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import re

from ckan.plugins import toolkit
from ckanext.attribution.model.crud import PackageQuery


def can_edit():
    '''
    Check editing permissions for updating agent directly.
    :return:
    '''
    try:
        permitted = toolkit.check_access('agent_update', {}, {})
        return permitted
    except toolkit.NotAuthorized:
        return False


def split_caps(string_input):
    return re.sub('(.)(?=[A-Z][^A-Z])', '\\1 ', string_input)


def get_contributions(pkg_id):
    '''
    Template access for the
    :func:`~ckanext.attribution.model.crud.PackageQuery.get_contributions` query method.
    :param pkg_id:
    :return:
    '''
    return PackageQuery.get_contributions(pkg_id)
