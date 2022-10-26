#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

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