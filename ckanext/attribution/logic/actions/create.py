#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.attribution.logic.actions.helpers import parse_contributors, get_author_string
from ckanext.attribution.model.crud import (AgentContributionActivityQuery, AgentQuery,
                                            ContributionActivityQuery,
                                            PackageContributionActivityQuery, AgentAffiliationQuery)


def agent_affiliation_create(context, data_dict):
    '''
    Create an :class:`~ckanext.attribution.model.agent_affiliation.AgentAffiliation` link record
    between two :class:`~ckanext.attribution.model.agent.Agent` records, e.g. to show institutional
    affiliation for an author.

    :param agent_a_id: ID of the first agent
    :type agent_a_id: str
    :param agent_b_id: ID of the second agent
    :type agent_b_id: str
    :param affiliation_type: type of affiliation/relationship between the two agents
    :type affiliation_type: str, optional
    :param description: description of affiliation/relationship
    :type description: str, optional
    :param start_date: when the affiliation started (e.g. when employment began)
    :type start_date: datetime.date, optional
    :param end_date: when the affiliation ended (e.g. when a researcher left an institution)
    :type end_date: datetime.date, optional
    :param context:
    :param data_dict:
    :returns: New agent affiliation record.
    :rtype: dict

    '''
    toolkit.check_access('agent_affiliation_create', context, data_dict)
    if 'agent_a_id' not in data_dict or 'agent_b_id' not in data_dict:
        raise toolkit.ValidationError('Two agent IDs are required.')
    for agent_id in [data_dict.get('agent_a_id'), data_dict.get('agent_b_id')]:
        try:
            toolkit.get_action('agent_show')(context, {
                'id': agent_id
            })
        except toolkit.ObjectNotFound:
            raise toolkit.ValidationError(
                'Agent ({0}) does not exist.'.format(agent_id))
    new_affiliation = AgentAffiliationQuery.create(**data_dict)
    if new_affiliation is None:
        raise toolkit.ValidationError('Unable to create affiliation. Check the fields are valid.')
    return new_affiliation.as_dict()


def agent_create(context, data_dict):
    '''
    Action for creating an :class:`~ckanext.attribution.model.agent.Agent` record. Different
    fields are required by different agent types.

    :param agent_type: broad type of agent; usually 'person' or 'org'
    :type agent_type: str
    :param family_name: family name of an person [person only, required]
    :type family_name: str, optional
    :param given_names: given name(s) or initials of an person [person only, required]
    :type given_names: str, optional
    :param given_names_first: whether given names should be displayed before the family name
                              (default True) [person only, optional]
    :type given_names_first: bool, optional
    :param user_id: the ID for a registered user of this CKAN instance associated with this agent
                    [person only, optional]
    :type user_id: str, optional
    :param name: name of an organisation [org only, required]
    :type name: str, optional
    :returns: New agent record.
    :rtype: dict

    '''
    toolkit.check_access('agent_create', context, data_dict)
    AgentQuery.validate(data_dict)
    new_agent = AgentQuery.create(**data_dict)
    if new_agent is None:
        raise toolkit.ValidationError('Unable to create agent. Check the fields are valid.')
    return new_agent.as_dict()


def contribution_activity_create(context, data_dict):
    '''
    Creates a :class:`~ckanext.attribution.model.contribution_activity.ContributionActivity`
    record, linked to a package and an agent via package_contribution_activity and
    agent_contribution_activity records (respectively). These link records are also created as part
    of this action, as the activity should not exist without the package or agent.

    :param package_id: the ID for the package this activity is associated with
    :type package_id: str
    :param agent_id: the ID for the agent this activity is associated with
    :type agent_id: str
    :param activity: short (one/two words) description for the activity
    :type activity: str
    :param scheme: name of the role/activity taxonomy, e.g. credit or datacite
    :type scheme: str
    :param level: lead, equal, or supporting
    :type level: str, optional
    :param time: time activity took place
    :type time: datetime.datetime, optional
    :param context:
    :param data_dict:
    :returns: New contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('contribution_activity_create', context, data_dict)
    # check for required fields
    package_id, agent_id = toolkit.get_or_bust(data_dict, ['package_id', 'agent_id'])
    try:
        toolkit.get_action('package_show')(context, {
            'id': package_id
        })
    except toolkit.ObjectNotFound:
        raise toolkit.ValidationError(
            'Cannot create activity for a package ({0}) that does not exist.'.format(package_id))
    try:
        toolkit.get_action('agent_show')(context, {
            'id': agent_id
        })
    except toolkit.ObjectNotFound:
        raise toolkit.ValidationError(
            'Cannot create activity for an agent ({0}) that does not exist.'.format(agent_id))
    new_activity = ContributionActivityQuery.create(**data_dict)
    PackageContributionActivityQuery.create(package_id=package_id,
                                            contribution_activity_id=new_activity.id)
    AgentContributionActivityQuery.create(agent_id=agent_id,
                                          contribution_activity_id=new_activity.id)
    return new_activity.as_dict()


@toolkit.chained_action
def package_create(next_func, context, data_dict):
    data_dict['author'] = 'pending'
    # we need the package ID to create links, but that's not created yet - so run the other
    # functions first
    created_pkg = next_func(context, data_dict)
    created_pkg['attribution'] = data_dict.get('attribution', '{}')
    parse_contributors(context, created_pkg)

    data_dict['author'] = get_author_string(package_id=created_pkg['id'])
    return data_dict
