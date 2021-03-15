#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.attribution.model.crud import (AgentAffiliationQuery, AgentContributionActivityQuery,
                                            AgentQuery, ContributionActivityQuery,
                                            PackageContributionActivityQuery)


def agent_affiliation_delete(context, data_dict):
    '''
    Delete an :class:`~ckanext.attribution.model.agent_affiliation.AgentAffiliation` record by ID.

    :param id: ID of the affiliation record
    :type id: str
    :returns: The affiliation record.
    :rtype: dict

    '''
    toolkit.check_access('agent_affiliation_delete', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return AgentAffiliationQuery.delete(item_id)


def agent_delete(context, data_dict):
    '''
    Delete an :class:`~ckanext.attribution.model.agent.Agent` record by ID.

    :param id: ID of the agent record
    :type id: str
    :returns: The agent record.
    :rtype: dict

    '''
    toolkit.check_access('agent_delete', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return AgentQuery.delete(item_id)


def agent_contribution_activity_delete(context, data_dict):
    '''
    Delete an
    :class:`~ckanext.attribution.model.agent_contribution_activity.AgentContributionActivity` record
    by ID.

    :param id: ID of the agent contribution activity record
    :type id: str
    :returns: The agent contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('agent_contribution_activity_delete', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return AgentContributionActivityQuery.delete(item_id)


def contribution_activity_delete(context, data_dict):
    '''
    Delete a :class:`~ckanext.attribution.model.contribution_activity.ContributionActivity`
    record by ID.

    :param id: ID of the contribution activity record
    :type id: str
    :returns: The contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('contribution_activity_delete', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return ContributionActivityQuery.delete(item_id)


def package_contribution_activity_delete(context, data_dict):
    '''
    Delete a
    :class:`~ckanext.attribution.model.package_contribution_activity.PackageContributionActivity`
    record by ID.

    :param id: ID of the package contribution activity record
    :type id: str
    :returns: The package contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('package_contribution_activity_delete', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    return PackageContributionActivityQuery.delete(item_id)
