#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.attribution.logic.actions.helpers import parse_contributors, get_author_string
from ckanext.attribution.model.crud import (AgentQuery,
                                            ContributionActivityQuery,
                                            AgentAffiliationQuery, AgentContributionActivityQuery)


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
    toolkit.check_access('agent_affiliation_update', context, data_dict)
    try:
        item_id = data_dict.pop('id')
    except KeyError:
        raise toolkit.ValidationError('Record ID must be provided.')
    # check agents exist if updating
    for agent_id in [data_dict.get('agent_a_id'), data_dict.get('agent_b_id')]:
        if agent_id is None:
            continue
        try:
            toolkit.get_action('agent_show')(context, {
                'id': agent_id
            })
        except toolkit.ObjectNotFound:
            raise toolkit.ValidationError(
                'Agent ({0}) does not exist.'.format(agent_id))
    affiliation = AgentAffiliationQuery.update(item_id, **data_dict)
    if affiliation is None:
        raise toolkit.ValidationError('Unable to update affiliation. Check the fields are valid.')
    return affiliation.as_dict()


def agent_update(context, data_dict):
    '''
    Action for updating an :class:`~ckanext.attribution.model.agent.Agent` record. Different
    fields are required by different agent types.

    :param id: ID of the record to update
    :type id: str
    :param agent_type: broad type of agent; usually 'person' or 'org'
    :type agent_type: str, optional
    :param family_name: family name of an person [person only]
    :type family_name: str, optional
    :param given_names: given name(s) or initials of an person [person only]
    :type given_names: str, optional
    :param given_names_first: whether given names should be displayed before the family name
                              (default True) [person only]
    :type given_names_first: bool, optional
    :param user_id: the ID for a registered user of this CKAN instance associated with this agent
                    [person only]
    :type user_id: str, optional
    :param name: name of an organisation [org only]
    :type name: str, optional
    :param context:
    :param data_dict:
    :returns: The updated agent record.
    :rtype: dict

    '''
    toolkit.check_access('agent_update', context, data_dict)
    try:
        item_id = data_dict.get('id')
    except KeyError:
        raise toolkit.ValidationError('Record ID must be provided.')
    current_record = AgentQuery.read(item_id)
    old_citation_name = current_record.citation_name
    if 'agent_type' not in data_dict:
        agent_type = current_record.agent_type
    else:
        agent_type = data_dict.get('agent_type')
    data_dict['agent_type'] = agent_type
    data_dict = AgentQuery.validate(data_dict)
    new_agent = AgentQuery.update(item_id, **data_dict)
    if new_agent.citation_name != old_citation_name:
        # if the name has been updated, the author strings need to be updated everywhere else too
        agent_id_column = AgentContributionActivityQuery.m.agent_id
        contrib_activities = AgentContributionActivityQuery.search(agent_id_column == item_id)
        packages = list(set([c.contribution_activity.package.id for c in contrib_activities]))
        for p in packages:
            author_string = get_author_string(package_id=p)
            toolkit.get_action('package_revise')({}, {'match': {'id': p},
                                                      'update': {'author': author_string}})
    if new_agent is None:
        raise toolkit.ValidationError('Unable to update agent. Check the fields are valid.')
    return new_agent.as_dict()


def agent_external_update(context, data_dict):
    '''
    Action for updating an :class:`~ckanext.attribution.model.agent.Agent` record by pulling
    information from an external source like ORCID or ROR.

    :param id: ID of the record to update
    :type id: str
    :returns: The updated agent record.
    :rtype: dict

    '''
    toolkit.check_access('agent_external_update', context, data_dict)
    try:
        item_id = data_dict.pop('id')
    except KeyError:
        raise toolkit.ValidationError('Record ID must be provided.')
    updated_dict = AgentQuery.read_from_external_api(item_id)
    updated_agent = AgentQuery.update(item_id, **updated_dict)
    if updated_agent is None:
        raise toolkit.ValidationError('Unable to update agent. Check the fields are valid.')
    return updated_agent.as_dict()


def contribution_activity_update(context, data_dict):
    '''
    Updates a :class:`~ckanext.attribution.model.contribution_activity.ContributionActivity`
    record, linked to a package and an agent via package_contribution_activity and
    agent_contribution_activity records (respectively). These link records are also updated as part
    of this action, as the activity should not exist without the package or agent.

    :param id: ID of the record to update
    :type id: str
    :param activity: short (one/two words) description for the activity
    :type activity: str, optional
    :param scheme: name of the role/activity taxonomy, e.g. credit or datacite
    :type scheme: str, optional
    :param level: lead, equal, or supporting
    :type level: str, optional
    :param time: time activity took place
    :type time: datetime.datetime, optional
    :param context:
    :param data_dict:
    :returns: New contribution activity record.
    :rtype: dict

    '''
    toolkit.check_access('contribution_activity_update', context, data_dict)
    item_id = toolkit.get_or_bust(data_dict, 'id')
    data_dict = ContributionActivityQuery.validate(data_dict)
    new_activity = ContributionActivityQuery.update(item_id, **data_dict)
    return new_activity.as_dict()


@toolkit.chained_action
def package_update(next_func, context, data_dict):
    parse_contributors(context, data_dict)
    data_dict['author'] = get_author_string(package_id=data_dict['id'])
    return next_func(context, data_dict)
