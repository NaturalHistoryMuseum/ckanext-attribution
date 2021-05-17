import itertools
import json

from ckan.plugins import toolkit
from ckanext.attribution.model.crud import (AgentQuery, AgentContributionActivityQuery,
                                            ContributionActivityQuery,
                                            AgentAffiliationQuery, PackageQuery)


def split_list_by_action(input_list, crud_model, id_field='id'):
    result = {
        'new': [],
        'updated': [],
        'deleted': []
    }
    for item in input_list:
        meta = item.get('meta', {})
        if meta.get('is_editing', False):
            # ignore anything where the changes haven't been saved
            continue
        is_hidden = meta.get('is_hidden', False)
        to_delete = meta.get('to_delete', False)
        is_active = not is_hidden and not to_delete

        is_new = meta.get('is_new', False)
        if is_active and is_new and item.get(id_field) is not None:
            # double check it's actually new - wrapped in an if so we don't have to check the
            # database for every single record
            try:
                crud_model.read(item.get(id_field))
                is_new = False
            except toolkit.ObjectNotFound:
                is_new = True

        if is_active and is_new:
            result['new'].append(item)
        elif is_active and meta.get('is_dirty', False):
            result['updated'].append(item)
        elif to_delete:
            result['deleted'].append(item)
    return result


def parse_contributors(context, data_dict):
    contributors = json.loads(data_dict.get('attribution', '{}'))

    try:
        pkg = PackageQuery.read(data_dict.get('id'))
    except:
        pkgs = PackageQuery.search(PackageQuery.m.name == data_dict.get('id'))
        pkg = pkgs[0] if len(pkgs) > 0 else None

    if pkg is None:
        raise toolkit.ObjectNotFound('This package does not exist.')
    pkg_id = pkg.id

    # agents
    agents = split_list_by_action(contributors.get('agents', []), AgentQuery)
    agent_cre = toolkit.get_action('agent_create')
    agent_upd = toolkit.get_action('agent_update')
    new_agents = {}
    for agent in agents['new']:
        gen_id = agent['id']
        del agent['id']
        new_id = agent_cre(context, agent)['id']
        new_agents[gen_id] = new_id
    for agent in agents['updated']:
        agent_upd(context, agent)
    # agents marked 'to_delete' almost certainly should not be deleted - only their activities
    # should be removed

    # activities
    activities = split_list_by_action(contributors.get('activities', []), ContributionActivityQuery)
    for agent in agents['deleted']:
        activities['deleted'] += [r.as_dict() for r in
                                  AgentContributionActivityQuery.read_agent_package(agent['id'],
                                                                                    pkg_id)]
    activities['deleted'] = list(set([a['id'] for a in activities['deleted']]))
    activity_cre = toolkit.get_action('contribution_activity_create')
    activity_upd = toolkit.get_action('contribution_activity_update')
    activity_del = toolkit.get_action('contribution_activity_delete')
    for activity in activities['new']:
        del activity['id']
        new_agent_id = new_agents.get(activity['agent_id'])
        if new_agent_id:
            activity['agent_id'] = new_agent_id
        activity['package_id'] = activity.get('package_id', pkg_id)
        activity_cre(context, activity)
    for activity in activities['updated']:
        activity_upd(context, activity)
    for activity in activities['deleted']:
        activity_del(context, {'id': activity})

    # citations (specialised activities)
    citations = split_list_by_action(contributors.get('citations', []), ContributionActivityQuery)
    citation_ids = []
    for citation in citations['new']:
        del citation['id']
        citation['activity'] = '[citation]'
        citation['scheme'] = 'internal'
        new_agent_id = new_agents.get(citation['agent_id'])
        if new_agent_id:
            citation['agent_id'] = new_agent_id
        citation['package_id'] = citation.get('package_id', pkg_id)
        new_citation = activity_cre(context, citation)
        citation_ids.append(new_citation['id'])
    for citation in citations['updated']:
        updated_citation = activity_upd(context, citation)
        citation_ids.append(updated_citation['id'])
    for citation in citations['deleted']:
        activity_del(context, {'id': citation['id']})

    # affiliations
    affiliations = split_list_by_action(contributors.get('affiliations', []), AgentAffiliationQuery,
                                        'db_id')

    def affiliation_key(x):
        return sorted((x['agent_id'], x['other_agent_id']))

    affiliations = {gk: [list(a)[0] for k, a in
                         itertools.groupby(sorted(gv, key=affiliation_key),
                                           key=affiliation_key)] for gk, gv in affiliations.items()}
    affiliation_cre = toolkit.get_action('agent_affiliation_create')
    affiliation_upd = toolkit.get_action('agent_affiliation_update')
    affiliation_del = toolkit.get_action('agent_affiliation_delete')

    for aff in affiliations['new']:
        del aff['id']
        new_agent_id = new_agents.get(aff['agent_id'])
        aff['agent_a_id'] = new_agent_id or aff['agent_id']
        new_other_agent_id = new_agents.get(aff['other_agent_id'])
        aff['agent_b_id'] = new_other_agent_id or aff['other_agent_id']
        aff['package_id'] = pkg_id
        affiliation_cre(context, aff)

    for aff in affiliations['updated']:
        aff['id'] = aff['db_id']
        new_agent_id = new_agents.get(aff['agent_id'])
        aff['agent_a_id'] = new_agent_id or aff['agent_id']
        new_other_agent_id = new_agents.get(aff['other_agent_id'])
        aff['agent_b_id'] = new_other_agent_id or aff['other_agent_id']
        affiliation_upd(context, aff)

    for aff in affiliations['deleted']:
        affiliation_del(context, {'id': aff['db_id']})

    return citation_ids


def get_author_string(package_id=None, citation_ids=None):
    if package_id is not None:
        citations = sorted([c for c in PackageQuery.get_contributions(package_id) if
                            c.activity == '[citation]'], key=lambda x: x.order)
    elif citation_ids is not None:
        citations = sorted([ContributionActivityQuery.read(c) for c in citation_ids],
                           key=lambda x: x.order)
    else:
        citations = []

    if len(citations) == 0:
        return toolkit.config.get('ckanext.doi.publisher',
                                  toolkit.config.get('ckan.site_title', 'Anonymous'))
    else:
        return '; '.join([c.agent.citation_name for c in citations])
