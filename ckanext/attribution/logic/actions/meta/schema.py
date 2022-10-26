#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckantools.validators import list_of_strings

from ckan.plugins import toolkit

# grab all the validator functions upfront
ignore_missing = toolkit.get_validator('ignore_missing')
not_missing = toolkit.get_validator('not_missing')
boolean_validator = toolkit.get_validator('boolean_validator')

# EXTRA ============================================================================================

attribution_controlled_lists = {
    'lists': [ignore_missing, list_of_strings()]
}

agent_external_search = {
    'q': [not_missing, str],
    'sources': [ignore_missing, list_of_strings()]
}

agent_external_read = {
    'agent_id': [ignore_missing, str],
    'external_id': [ignore_missing, str],
    'external_id_scheme': [ignore_missing, str],
    'diff': [ignore_missing, boolean_validator]
}

validate_external_id = {
    'external_id': [not_missing, str],
    'external_id_scheme': [not_missing, str]
}
