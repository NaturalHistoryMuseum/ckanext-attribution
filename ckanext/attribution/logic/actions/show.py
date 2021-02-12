#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.attribution.model.crud import (AgentAffiliationQuery, AgentContributionActivityQuery,
                                            AgentQuery, ContributionActivityQuery,
                                            PackageContributionActivityQuery)


@toolkit.side_effect_free
def agent_affiliation_show(context, data_dict):
    '''
    Retrieve an :class:`~ckanext.attribution.model.agent_affiliation.AgentAffiliation` record by ID.

    :param id: ID of the affiliation record
    :type id: str
    :param context:
    :param data_dict:
    :returns: The affiliation record.
    :rtype: dict

    '''
    toolkit.check_access(u'agent_affiliation_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, u'id')
    return AgentAffiliationQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def agent_show(context, data_dict):
    '''
    Retrieve an :class:`~ckanext.attribution.model.agent.Agent` record by ID.

    :param id: ID of the agent record
    :type id: str
    :param context:
    :param data_dict:
    :returns: The agent record.
    :rtype: dict

    '''
    toolkit.check_access(u'agent_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, u'id')
    return AgentQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def agent_contribution_activity_show(context, data_dict):
    '''
    Retrieve an
    :class:`~ckanext.attribution.model.agent_contribution_activity.AgentContributionActivity` record
    by ID.

    :param id: ID of the agent contribution activity record
    :type id: str
    :param context:
    :param data_dict:
    :returns: The agent contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access(u'agent_contribution_activity_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, u'id')
    return AgentContributionActivityQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def contribution_activity_show(context, data_dict):
    '''
    Retrieve a :class:`~ckanext.attribution.model.contribution_activity.ContributionActivity`
    record by ID.

    :param id: ID of the contribution activity record
    :type id: str
    :param context:
    :param data_dict:
    :returns: The contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access(u'contribution_activity_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, u'id')
    return ContributionActivityQuery.read(item_id).as_dict()


@toolkit.side_effect_free
def package_contribution_activity_show(context, data_dict):
    '''
    Retrieve a
    :class:`~ckanext.attribution.model.package_contribution_activity.PackageContributionActivity`
    record by ID.

    :param id: ID of the package contribution activity record
    :type id: str
    :param context:
    :param data_dict:
    :returns: The package contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access(u'package_contribution_activity_show', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, u'id')
    return PackageContributionActivityQuery.read(item_id).as_dict()
