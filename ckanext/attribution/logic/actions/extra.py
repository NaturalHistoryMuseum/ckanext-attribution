#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.attribution.lib.orcid_api import OrcidApi
from ckanext.attribution.lib.ror_api import RorApi
from ckanext.attribution.model.crud import AgentQuery


@toolkit.side_effect_free
def contribution_roles_list(context, data_dict):
    '''
    List translated available contribution roles from the CRediT schema (https://credit.niso.org).
    :returns: Dict of translated roles and the standard CRediT role name.
    :rtype: dict

    '''
    return {
        toolkit._('Conceptualization'): 'Conceptualization',
        toolkit._('Data curation'): 'Data curation',
        toolkit._('Formal analysis'): 'Formal analysis',
        toolkit._('Funding acquisition'): 'Funding acquisition',
        toolkit._('Investigation'): 'Investigation',
        toolkit._('Methodology'): 'Methodology',
        toolkit._('Project administration'): 'Project administration',
        toolkit._('Resources'): 'Resources',
        toolkit._('Software'): 'Software',
        toolkit._('Supervision'): 'Supervision',
        toolkit._('Validation'): 'Validation',
        toolkit._('Visualization'): 'Visualization',
        toolkit._('Writing – original draft'): 'Writing – original draft',
        toolkit._('Writing – review & editing'): 'Writing – review & editing',
    }


@toolkit.side_effect_free
def external_id_schemes(context, data_dict):
    return {
        'orcid': {
            'url': 'https://orcid.org/{0}',
            'label': 'ORCID',
            'agent_types': ['individual'],
            'default': ['individual']
        },
        'ror': {
            'url': 'https://ror.org/{0}',
            'label': 'ROR',
            'agent_types': ['org'],
            'default': ['org']
        }
    }


@toolkit.side_effect_free
def agent_external_search(context, data_dict):
    '''
    Search external sources for agent data. Ignores records that already exist in the database.

    :param q: searches all fields (names, ids, etc)
    :type q: str
    :param sources: a list of sources to search (default None searches all)
    :type sources: list, optional
    :returns: A list of potential matches.
    :rtype: list

    '''
    toolkit.check_access('agent_show', context, data_dict)
    q = toolkit.get_or_bust(data_dict, 'q')
    sources = data_dict.get('sources')
    if sources is not None:
        sources = [s.lower() for s in sources]
    results = {}
    if q is None or q == '':
        return results

    # ORCID
    if sources is None or 'orcid' in sources:
        orcid_remaining = 0
        orcidapi = OrcidApi()
        orcid_search = orcidapi.search(q=q)
        n = orcid_search.get(u'total', 0)
        orcid_records = orcid_search.get('records')
        orcid_records = [r for r in orcid_records if
                         AgentQuery.read_external_id(r['external_id']) is None]
        if n > len(orcid_records):
            orcid_remaining = n - len(orcid_records)
        results['orcid'] = {'records': orcid_records,
                            'remaining': orcid_remaining}

    # ROR
    if sources is None or 'ror' in sources:
        ror_remaining = 0
        rorapi = RorApi()
        ror_search = rorapi.search(q=q)
        n = ror_search.get(u'total', 0)
        ror_records = ror_search.get('records')
        ror_records = [r for r in ror_records if
                       AgentQuery.read_external_id(r['external_id']) is None]
        if n > len(ror_records):
            ror_remaining = n - len(ror_records)
        results['ror'] = {'records': ror_records,
                          'remaining': ror_remaining}

    return results
