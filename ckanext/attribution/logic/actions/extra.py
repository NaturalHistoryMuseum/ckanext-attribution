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
def attribution_controlled_lists(context, data_dict):
    '''
    Return one or more lists or dicts of defined values, e.g. agent types or contribution activity
    types. Details dicts can include various pieces of arbitrary information (e.g. names,
    translations, or icon definitions for templates) as long as the initial structure is retained.

    :param lists: names of the lists to be returned
    :type lists: list, optional
    :return: dict of all requested lists (or all lists if unspecified)
    :rtype: dict
    '''
    all_lists = {
        'agent_types': {'person': {'fa_icon': 'fas fa-user',
                                   'default_scheme': 'orcid'},
                        'org': {'fa_icon': 'fas fa-building',
                                'default_scheme': 'ror'},
                        'other': {'fa_icon': 'fas fa-asterisk',
                                  'default_scheme': None}},
        'contribution_activity_types': {
            'credit': [{'name': 'Conceptualization'},
                       {'name': 'Data curation'},
                       {'name': 'Formal analysis'},
                       {'name': 'Funding acquisition'},
                       {'name': 'Investigation'},
                       {'name': 'Methodology'},
                       {'name': 'Project administration'},
                       {'name': 'Resources'},
                       {'name': 'Software'},
                       {'name': 'Supervision'},
                       {'name': 'Validation'},
                       {'name': 'Visualization'},
                       {'name': 'Writing – original draft'},
                       {'name': 'Writing – review & editing'}],
            'datacite': [
                {'name': 'ContactPerson'},
                {'name': 'DataCollector'},
                {'name': 'DataCurator'},
                {'name': 'DataManager'},
                {'name': 'Distributor'},
                {'name': 'Editor'},
                {'name': 'HostingInstitution'},
                {'name': 'Other'},
                {'name': 'Producer'},
                {'name': 'ProjectLeader'},
                {'name': 'ProjectManager'},
                {'name': 'ProjectMember'},
                {'name': 'RegistrationAgency'},
                {'name': 'RegistrationAuthority'},
                {'name': 'RelatedPerson'},
                {'name': 'ResearchGroup'},
                {'name': 'RightsHolder'},
                {'name': 'Researcher'},
                {'name': 'Sponsor'},
                {'name': 'Supervisor'},
                {'name': 'WorkPackageLeader'},
            ]
        },
        'contribution_activity_levels': ['Lead', 'Supporting', 'Equal'],
        'agent_external_id_schemes': {
            'orcid': {
                'url': 'https://orcid.org/{0}',
                'scheme_uri': 'https://orcid.org',
                'label': 'ORCID',
                'fa_icon': 'fab fa-orcid'

            },
            'ror': {
                'url': 'https://ror.org/{0}',
                'scheme_uri': 'https://ror.org',
                'label': 'ROR',
                'fa_icon': 'fas fa-university'
            }
        }
    }
    lists = data_dict.get('lists')
    if lists is not None and isinstance(lists, str):
        lists = [l.strip() for l in lists.split(',')]
    if lists is not None and isinstance(lists, list):
        lists = [l for l in lists if l in all_lists]
        return {k: v for k, v in all_lists.items() if k in lists}
    else:
        return all_lists


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


@toolkit.side_effect_free
def agent_external_read(context, data_dict):
    '''
    Read data for a record from an external source like ORCID or ROR.

    :param id: ID of the record to read
    :type id: str
    :param diff: only show values that differ from the record's current values (default False)
    :type diff: bool, optional
    :returns: The details pulled from the external source, formatted as a record dict
    :rtype: dict

    '''
    toolkit.check_access('agent_show', context, data_dict)
    try:
        item_id = data_dict.pop('id')
    except KeyError:
        raise toolkit.ValidationError('Record ID must be provided.')
    diff = toolkit.asbool(data_dict.get('diff', False))
    updated_dict = AgentQuery.read_from_external_api(item_id)
    updated_dict['id'] = item_id
    del updated_dict['user_id']  # this is internal only so it's always going to be None
    if diff:
        item_dict = AgentQuery.read(item_id).as_dict()
        for k, v in item_dict.items():
            if k in updated_dict and updated_dict.get(k) == v:
                del updated_dict[k]
    return updated_dict
