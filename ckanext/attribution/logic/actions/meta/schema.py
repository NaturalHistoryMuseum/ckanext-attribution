#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit

# grab all the validator functions upfront
ignore_missing = toolkit.get_validator('ignore_missing')
not_missing = toolkit.get_validator('not_missing')
boolean_validator = toolkit.get_validator('boolean_validator')
isodate_validator = toolkit.get_validator('isodate')
int_validator = toolkit.get_validator('int_validator')
unicode_safe = toolkit.get_validator("unicode_safe")
list_of_strings = toolkit.get_validator("list_of_strings")

# CREATE ===========================================================================================

agent_affiliation_create = {
    'agent_a_id': [not_missing, unicode_safe],
    'agent_b_id': [not_missing, unicode_safe],
    'affiliation_type': [ignore_missing, unicode_safe],
    'description': [ignore_missing, unicode_safe],
    'start_date': [ignore_missing, isodate_validator],
    'end_date': [ignore_missing, isodate_validator],
}

agent_create = {
    'agent_type': [not_missing, unicode_safe],
    'family_name': [ignore_missing, unicode_safe],
    'given_names': [ignore_missing, unicode_safe],
    'given_names_first': [ignore_missing, boolean_validator],
    'user_id': [ignore_missing, unicode_safe],
    'name': [ignore_missing, unicode_safe],
}

contribution_activity_create = {
    'package_id': [not_missing, unicode_safe],
    'agent_id': [not_missing, unicode_safe],
    'activity': [not_missing, unicode_safe],
    'scheme': [not_missing, unicode_safe],
    'level': [ignore_missing, unicode_safe],
    'time': [ignore_missing, isodate_validator],
}

# DELETE ===========================================================================================

agent_affiliation_delete = {'id': [not_missing, unicode_safe]}

agent_delete = {'id': [not_missing, unicode_safe]}

agent_contribution_activity_delete = {'id': [not_missing, unicode_safe]}

contribution_activity_delete = {
    'id': [not_missing, unicode_safe],
}

package_contribution_activity_delete = {'id': [not_missing, unicode_safe]}

# EXTRA ============================================================================================

attribution_controlled_lists = {'lists': [ignore_missing, list_of_strings]}

agent_external_search = {
    'q': [not_missing, unicode_safe],
    'sources': [ignore_missing, list_of_strings],
}

agent_external_read = {
    'agent_id': [ignore_missing, unicode_safe],
    'external_id': [ignore_missing, unicode_safe],
    'external_id_scheme': [ignore_missing, unicode_safe],
    'diff': [ignore_missing, boolean_validator],
}

validate_external_id = {
    'external_id': [not_missing, unicode_safe],
    'external_id_scheme': [not_missing, unicode_safe],
}

# SHOW =============================================================================================

agent_affiliation_show = {'id': [not_missing, unicode_safe]}

agent_show = {'id': [not_missing, unicode_safe]}

agent_list = {
    'q': [ignore_missing, unicode_safe],
    'mode': [ignore_missing, unicode_safe],
}

agent_contribution_activity_show = {'id': [not_missing, unicode_safe]}

contribution_activity_show = {'id': [not_missing, unicode_safe]}

package_contribution_activity_show = {'id': [not_missing, unicode_safe]}

package_contributions_show = {
    'id': [not_missing, unicode_safe],
    'limit': [ignore_missing, int_validator],
    'offset': [ignore_missing, int_validator],
}

agent_affiliations = {
    'agent_id': [not_missing, unicode_safe],
    'package_id': [ignore_missing, unicode_safe],
}

# UPDATE ===========================================================================================

agent_affiliation_update = {
    'id': [not_missing, unicode_safe],
    'agent_a_id': [ignore_missing, unicode_safe],
    'agent_b_id': [ignore_missing, unicode_safe],
    'affiliation_type': [ignore_missing, unicode_safe],
    'description': [ignore_missing, unicode_safe],
    'start_date': [ignore_missing, isodate_validator],
    'end_date': [ignore_missing, isodate_validator],
}

agent_update = {
    'id': [not_missing, unicode_safe],
    'agent_type': [ignore_missing, unicode_safe],
    'family_name': [ignore_missing, unicode_safe],
    'given_names': [ignore_missing, unicode_safe],
    'given_names_first': [ignore_missing, boolean_validator],
    'user_id': [ignore_missing, unicode_safe],
    'name': [ignore_missing, unicode_safe],
}

agent_external_update = {'id': [not_missing, unicode_safe]}

contribution_activity_update = {
    'id': [not_missing, unicode_safe],
    'activity': [ignore_missing, unicode_safe],
    'scheme': [ignore_missing, unicode_safe],
    'level': [ignore_missing, unicode_safe],
    'time': [ignore_missing, isodate_validator],
}
