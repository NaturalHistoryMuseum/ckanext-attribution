#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.attribution.model.crud import (AgentContributionActivityQuery, AgentQuery,
                                            ContributionActivityQuery,
                                            PackageContributionActivityQuery, AgentAffiliationQuery)


def agent_affiliation_update(context, data_dict):
    '''
    Update an :class:`~ckanext.attribution.model.agent_affiliation.AgentAffiliation` link record.

    :param id: ID of the record to update
    :type id: str
    :param agent_a_id: ID of the first agent
    :type agent_a_id: str, optional
    :param agent_b_id: ID of the second agent
    :type agent_b_id: str, optional
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
    :returns: The updated agent affiliation record.
    :rtype: dict

    '''
    toolkit.check_access(u'agent_affiliation_update', context, data_dict)
    try:
        item_id = data_dict.pop(u'id')
    except KeyError:
        raise toolkit.ValidationError(u'Record ID must be provided.')
    # check agents exist if updating
    for agent_id in [data_dict.get(u'agent_a_id'), data_dict.get(u'agent_b_id')]:
        if agent_id is None:
            continue
        try:
            toolkit.get_action(u'agent_show')(context, {
                u'id': agent_id
            })
        except toolkit.ObjectNotFound:
            raise toolkit.ValidationError(
                u'Agent ({0}) does not exist.'.format(agent_id))
    affiliation = AgentAffiliationQuery.update(item_id, **data_dict)
    if affiliation is None:
        raise toolkit.ValidationError(u'Unable to update affiliation. Check the fields are valid.')
    return affiliation.as_dict()


def agent_update(context, data_dict):
    '''
    Action for updating an :class:`~ckanext.attribution.model.agent.Agent` record. Different
    fields are required by different agent types.

    :param id: ID of the record to update
    :type id: str
    :param agent_type: broad type of agent; usually 'individual' or 'org'
    :type agent_type: str, optional
    :param family_name: family name of an individual [individual only]
    :type family_name: str, optional
    :param given_names: given name(s) or initials of an individual [individual only]
    :type given_names: str, optional
    :param given_names_first: whether given names should be displayed before the family name
                              (default True) [individual only]
    :type given_names_first: bool, optional
    :param orcid: an individual's `ORCID <https://orcid.org>`_ [individual only]
    :type orcid: str, optional
    :param user_id: the ID for a registered user of this CKAN instance associated with this agent
                    [individual only]
    :type user_id: str, optional
    :param name: name of an organisation [org only]
    :type name: str, optional
    :param ror_id: an organisation's `ROR <https://ror.org>`_ ID [org only]
    :type ror_id: str, optional
    :param context: 
    :param data_dict: 
    :returns: The updated agent record.
    :rtype: dict

    '''
    toolkit.check_access(u'agent_update', context, data_dict)
    try:
        item_id = data_dict.pop(u'id')
    except KeyError:
        raise toolkit.ValidationError(u'Record ID must be provided.')
    current_record = AgentQuery.read(item_id)
    if u'agent_type' not in data_dict:
        change_agent_type = False
        agent_type = current_record.agent_type
    else:
        change_agent_type = True
        agent_type = data_dict.get(u'agent_type')
    if agent_type == 'individual':
        required = [u'family_name', u'given_names']
        optional = [u'given_names_first', u'orcid', u'user_id']
    elif agent_type == 'org':
        required = [u'name']
        optional = [u'ror_id']
    else:
        required = []
        optional = []
    for k in required:
        if k not in data_dict:
            raise toolkit.ValidationError(u'{0} is a required field.'.format(k))
    all_fields = required + optional
    if len(all_fields) > 0:
        for k in data_dict:
            if k not in all_fields:
                raise toolkit.ValidationError(
                    u'{0} is not a valid field for the "{1}" agent type.'.format(k, agent_type))
    new_agent = AgentQuery.update(**data_dict)
    if new_agent is None:
        raise toolkit.ValidationError(u'Unable to update agent. Check the fields are valid.')
    return new_agent.as_dict()


def contribution_activity_update(context, data_dict):
    '''
    Updates a :class:`~ckanext.attribution.model.contribution_activity.ContributionActivity`
    record, linked to a package and an agent via package_contribution_activity and
    agent_contribution_activity records (respectively). These link records are also updated as part
    of this action, as the activity should not exist without the package or agent.

    :param id: ID of the record to update
    :type id: str
    :param package_id: the ID for the package this activity is associated with
    :type package_id: str
    :param agent_id: the ID for the agent this activity is associated with
    :type agent_id: str
    :param activity: short (one/two words) description for the activity
    :type activity: str
    :param level: lead, equal, or supporting
    :type level: str, optional
    :param time: time activity took place
    :type time: datetime.datetime, optional
    :param context: 
    :param data_dict: 
    :returns: New contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access(u'contribution_activity_update', context, data_dict)
    try:
        item_id = data_dict.pop(u'id')
    except KeyError:
        raise toolkit.ValidationError(u'Record ID must be provided.')
    # check for required fields
    package_id, agent_id = toolkit.get_or_bust(data_dict, [u'package_id', u'agent_id'])
    try:
        toolkit.get_action(u'package_show')(context, {
            u'id': package_id
        })
    except toolkit.ObjectNotFound:
        raise toolkit.ValidationError(
            u'Cannot update activity for a package ({0}) that does not exist.'.format(package_id))
    try:
        toolkit.get_action(u'agent_show')(context, {
            u'id': agent_id
        })
    except toolkit.ObjectNotFound:
        raise toolkit.ValidationError(
            u'Cannot update activity for an agent ({0}) that does not exist.'.format(agent_id))
    new_activity = ContributionActivityQuery.update(**data_dict)
    PackageContributionActivityQuery.update(package_id=package_id,
                                            contribution_activity_id=new_activity.id)
    AgentContributionActivityQuery.update(agent_id=agent_id,
                                          contribution_activity_id=new_activity.id)
    return new_activity.as_dict()
