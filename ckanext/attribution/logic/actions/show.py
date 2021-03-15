#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

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
        portal_results = [a.as_dict() for a in AgentQuery.all()]
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
    contributions_dict = [{'contribution_activity': a.as_dict(), 'agent': a.agent.as_dict()} for v
                          in contributions.values() for a in v]
    return contributions_dict


@toolkit.side_effect_free
def agent_all_affiliations(context, data_dict):
    toolkit.check_access('agent_show', context, data_dict)
    toolkit.check_access('agent_affiliation_show', context, data_dict)
    agent_id = toolkit.get_or_bust(data_dict, 'agent_id')
    agent = AgentQuery.read(agent_id)
    return [{k: v.as_dict() for k, v in a.items()} for a in agent.affiliations]
