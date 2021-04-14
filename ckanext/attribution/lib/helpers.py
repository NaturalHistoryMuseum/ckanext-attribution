#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools
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


def get_cited_contributors(pkg_id):
    contributions = PackageQuery.get_contributions(pkg_id)
    by_agent = {k: list(v) for k, v in
                itertools.groupby(sorted(contributions, key=lambda x: x.agent.id),
                                  key=lambda x: x.agent.id)}

    def _is_cited(entry):
        return any([a.activity == '[citation]' for a in entry[1]])

    def _citation_order(entry):
        activities = entry[1]
        citation = [a.order for a in activities if a.activity == '[citation]']
        if citation:
            return max(citation)
        else:
            return -1

    def _format_entries(entry_list):
        return [{'agent': c[1][0].agent,
                 'contributions': [a for a in c[1] if a.activity != '[citation]']} for c in
                entry_list]

    cited_agents = {'cited' if k else 'uncited': _format_entries(v) for k, v in
                    itertools.groupby(sorted(by_agent.items(), key=_citation_order),
                                      key=_is_cited)}
    return cited_agents


def controlled_list(list_name):
    return toolkit.get_action('attribution_controlled_lists')({}, {'lists': [list_name]})[list_name]
