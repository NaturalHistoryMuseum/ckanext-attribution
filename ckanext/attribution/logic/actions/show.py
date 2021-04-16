#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools

from ckan.plugins import toolkit
from ckanext.attribution.model.crud import (AgentAffiliationQuery, AgentContributionActivityQuery,
                                            AgentQuery, ContributionActivityQuery,
                                            PackageContributionActivityQuery, PackageQuery)
from sqlalchemy import or_


@toolkit.side_effect_free
def agent_affiliation_show(context, data_dict):
    '''
    Retrieve an :class:`~ckanext.attribution.model.agent_affiliation.AgentAffiliation` record by ID.

    :param id: ID of the affiliation record
    :type id: str
    :returns: The affiliation record.
    :rtype: dict

    '''
    toolkit.check_access('agent_affiliation_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return AgentAffiliationQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def agent_show(context, data_dict):
    '''
    Retrieve an :class:`~ckanext.attribution.model.agent.Agent` record by ID.

    :param id: ID of the agent record
    :type id: str
    :returns: The agent record.
    :rtype: dict

    '''
    toolkit.check_access('agent_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return AgentQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def agent_list(context, data_dict):
    '''
    Search for :class:`~ckanext.attribution.model.agent.Agent` records.

    :param q: name or external id (ORCID/ROR ID) of the agent record
    :type q: str, optional
    :returns: A list of potential matches.
    :rtype: list

    '''
    toolkit.check_access('agent_show', context, data_dict)
    q = data_dict.get('q')
    if q is not None and q != '':
        q_string = '{0}%'.format(q)
        name_cols = [AgentQuery.m.name,
                     AgentQuery.m.family_name,
                     AgentQuery.m.given_names]
        name_parts = [subq for c in name_cols for subq in
                      [c.ilike('{0}%'.format(p)) for p in q.split(' ')]]
        q_parts = [*name_parts,
                   AgentQuery.m.external_id.ilike(q_string)]
        portal_results = AgentQuery.search(or_(*q_parts))
    else:
        portal_results = AgentQuery.all()
    results = [a.as_dict() for a in portal_results]
    return results


@toolkit.side_effect_free
def agent_contribution_activity_show(context, data_dict):
    '''
    Retrieve an
    :class:`~ckanext.attribution.model.agent_contribution_activity.AgentContributionActivity` record
    by ID.

    :param id: ID of the agent contribution activity record
    :type id: str
    :returns: The agent contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('agent_contribution_activity_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return AgentContributionActivityQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def contribution_activity_show(context, data_dict):
    '''
    Retrieve a :class:`~ckanext.attribution.model.contribution_activity.ContributionActivity`
    record by ID.

    :param id: ID of the contribution activity record
    :type id: str
    :returns: The contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('contribution_activity_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return ContributionActivityQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def package_contribution_activity_show(context, data_dict):
    '''
    Retrieve a
    :class:`~ckanext.attribution.model.package_contribution_activity.PackageContributionActivity`
    record by ID.

    :param id: ID of the package contribution activity record
    :type id: str
    :returns: The package contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('package_contribution_activity_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return PackageContributionActivityQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def package_contributions_show(context, data_dict):
    '''
    Show associated agents and their contributions for a given package.

    :param id: ID of the package record
    :type id: str
    :returns: The package contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('package_contributions_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    contributions = PackageQuery.get_contributions(item_id)
    by_agent = {k: list(v) for k, v in
                itertools.groupby(sorted(contributions, key=lambda x: x.agent.id),
                                  key=lambda x: x.agent.id)}
    contributions_dict = [
        {
            'agent': v[0].agent.as_dict(),
            'activities': [a.as_dict() for a in v],
            'affiliations': toolkit.get_action('agent_affiliations')(context,
                                               {'agent_id': k, 'package_id': item_id})
        } for k, v in by_agent.items()]
    return contributions_dict


@toolkit.side_effect_free
def agent_affiliations(context, data_dict):
    '''
    Show affiliated agents, either all or for a given package. Including a package ID will still
    return 'global' affiliations, e.g. those with no specific package associated.

    :param agent_id: ID of the agent
    :type agent_id: str
    :param package_id: ID of the package
    :type package_id: str, optional
    :returns: The package contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('agent_show', context, data_dict)
    toolkit.check_access('agent_affiliation_show', context, data_dict)
    agent_id = toolkit.get_or_bust(data_dict, 'agent_id')
    package_id = data_dict.get('package_id')
    agent = AgentQuery.read(agent_id)
    affiliations = agent.affiliations
    if package_id is not None:
        affiliations = [a for a in affiliations if a['affiliation'].package_id is None or a[
            'affiliation'].package_id == package_id]

    def _transform(a):
        detail = a.get('affiliation').as_dict()
        try:
            del detail['agent_a_id']
        except KeyError:
            pass
        try:
            del detail['agent_b_id']
        except KeyError:
            pass
        detail['other_agent'] = a.get('agent').as_dict()
        return detail

    return [_transform(a) for a in affiliations]
