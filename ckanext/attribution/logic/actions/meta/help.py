#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

# CREATE ===========================================================================================

agent_affiliation_create = '''
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
:returns: New agent affiliation record.
:rtype: dict
'''

agent_create = '''
Action for creating an :class:`~ckanext.attribution.model.agent.Agent` record. Different fields are
required by different agent types.

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

contribution_activity_create = '''
Creates a :class:`~ckanext.attribution.model.contribution_activity.ContributionActivity` record,
linked to a package and an agent via package_contribution_activity and agent_contribution_activity
records (respectively). These link records are also created as part of this action, as the activity
should not exist without the package or agent.

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
:returns: New contribution activity record.
:rtype: dict
'''

# EXTRA ============================================================================================

attribution_controlled_lists = '''
Return one or more lists or dicts of defined values, e.g. agent types or contribution activity
types. Details dicts can include various pieces of arbitrary information (e.g. names,
translations, or icon definitions for templates) as long as the initial structure is retained.

:param lists: names of the lists to be returned
:type lists: list, optional
:return: dict of all requested lists (or all lists if unspecified)
:rtype: dict
'''

agent_external_search = '''
Search external sources for agent data. Ignores records that already exist in the database.

:param q: searches all fields (names, ids, etc)
:type q: str
:param sources: a list of sources to search (default None searches all)
:type sources: list, optional
:returns: A list of potential matches.
:rtype: list
'''

agent_external_read = '''
Read data from an external source like ORCID or ROR.

:param agent_id: ID of the record to read
:type agent_id: str, optional
:param external_id: ID from external service
:type external_id: str, optional
:param external_id_scheme: external scheme, e.g. orcid
:type external_id_scheme: str, optional
:param diff: only show values that differ from the record's current values; only valid if record
             already exists (default False)
:type diff: bool, optional
:returns: The details pulled from the external source, formatted as a record dict
:rtype: dict
'''

validate_external_id = '''
Validate/format an external ID.

:param external_id: ID from external service
:type external_id: str
:param external_id_scheme: external scheme, e.g. orcid
:type external_id_scheme: str
:return:
'''