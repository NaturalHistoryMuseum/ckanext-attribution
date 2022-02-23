#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import SingletonPlugin, implements, interfaces, toolkit
from ckanext.attribution.lib import helpers
from ckanext.attribution.model import (agent, agent_affiliation, agent_contribution_activity,
                                       contribution_activity, package_contribution_activity,
                                       relationships)
from ckanext.attribution.commands import cli

try:
    from ckanext.doi.interfaces import IDoi

    doi_available = True
except ImportError:
    doi_available = False


class AttributionPlugin(SingletonPlugin):
    '''A CKAN extension that adds support for complex attribution.'''

    implements(interfaces.IActions, inherit=True)
    implements(interfaces.IAuthFunctions, inherit=True)
    implements(interfaces.IClick)
    implements(interfaces.IConfigurable)
    implements(interfaces.IConfigurer)
    implements(interfaces.IFacets, inherit=True)
    implements(interfaces.IPackageController, inherit=True)
    implements(interfaces.ITemplateHelpers)
    if doi_available:
        implements(IDoi, inherit=True)

    # IActions
    def get_actions(self):
        from ckanext.attribution.logic.actions import create, show, update, delete, extra
        actions = {
            'agent_affiliation_create': create.agent_affiliation_create,
            'agent_create': create.agent_create,
            'contribution_activity_create': create.contribution_activity_create,
            'package_create': create.package_create,
            'agent_affiliation_show': show.agent_affiliation_show,
            'agent_show': show.agent_show,
            'agent_list': show.agent_list,
            'agent_contribution_activity_show': show.agent_contribution_activity_show,
            'contribution_activity_show': show.contribution_activity_show,
            'package_contribution_activity_show': show.package_contribution_activity_show,
            'package_contributions_show': show.package_contributions_show,
            'agent_affiliations': show.agent_affiliations,
            'agent_affiliation_update': update.agent_affiliation_update,
            'agent_update': update.agent_update,
            'agent_external_update': update.agent_external_update,
            'contribution_activity_update': update.contribution_activity_update,
            'package_update': update.package_update,
            'agent_affiliation_delete': delete.agent_affiliation_delete,
            'agent_delete': delete.agent_delete,
            'agent_contribution_activity_delete': delete.agent_contribution_activity_delete,
            'contribution_activity_delete': delete.contribution_activity_delete,
            'package_contribution_activity_delete': delete.package_contribution_activity_delete,
            'attribution_controlled_lists': extra.attribution_controlled_lists,
            'agent_external_search': extra.agent_external_search,
            'agent_external_read': extra.agent_external_read,
            'validate_external_id': extra.validate_external_id
        }
        return actions

    # IAuthFunctions
    def get_auth_functions(self):
        from ckanext.attribution.logic.auth import create, show, update, delete
        auth = {
            'agent_affiliation_create': create.agent_affiliation_create,
            'agent_create': create.agent_create,
            'contribution_activity_create': create.contribution_activity_create,
            'agent_affiliation_show': show.agent_affiliation_show,
            'agent_show': show.agent_show,
            'agent_contribution_activity_show': show.agent_contribution_activity_show,
            'contribution_activity_show': show.contribution_activity_show,
            'package_contribution_activity_show': show.package_contribution_activity_show,
            'package_contributions_show': show.package_contributions_show,
            'agent_affiliation_update': update.agent_affiliation_update,
            'agent_update': update.agent_update,
            'agent_external_update': update.agent_external_update,
            'contribution_activity_update': update.contribution_activity_update,
            'agent_affiliation_delete': delete.agent_affiliation_delete,
            'agent_delete': delete.agent_delete,
            'agent_contribution_activity_delete': delete.agent_contribution_activity_delete,
            'contribution_activity_delete': delete.contribution_activity_delete,
            'package_contribution_activity_delete': delete.package_contribution_activity_delete,
        }
        return auth

    # IClick
    def get_commands(self):
        return cli.get_commands()

    # IConfigurable
    def configure(self, config):
        contribution_activity.check_for_table()
        agent.check_for_table()
        agent_affiliation.check_for_table()
        agent_contribution_activity.check_for_table()
        package_contribution_activity.check_for_table()
        relationships.setup_relationships()

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'theme/templates')
        toolkit.add_resource('theme/assets', 'ckanext-attribution')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        enable_faceting = toolkit.asbool(
            toolkit.config.get('ckanext.attribution.enable_faceting', False))
        if enable_faceting:
            facets_dict['author'] = toolkit._('Contributors')
        return facets_dict

    # IPackageController
    def before_index(self, pkg_dict):
        enable_faceting = toolkit.asbool(
            toolkit.config.get('ckanext.attribution.enable_faceting', False))
        if enable_faceting:
            contributions = toolkit.get_action('package_contributions_show')({}, {'id': pkg_dict['id']})
            agents = [c['agent'] for c in contributions['contributions']]
            pkg_dict['author'] = [a['display_name'] for a in agents]
        return pkg_dict

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_contributions': helpers.get_contributions,
            'can_edit': helpers.can_edit,
            'split_caps': helpers.split_caps,
            'get_cited_contributors': helpers.get_cited_contributors,
            'controlled_list': helpers.controlled_list,
            'doi_plugin': helpers.doi_plugin,
            'agent_from_user': helpers.agent_from_user
        }

    # IDoi
    def build_metadata_dict(self, pkg_dict, metadata_dict, errors):
        # Adds cited contributors as 'creators' and uncited contributors as 'contributors'.
        # 'creators' do not get roles/contributor types; 'contributors' do.
        all_contributors = helpers.get_cited_contributors(pkg_dict['id'])
        id_schemes = helpers.controlled_list('agent_external_id_schemes')

        def _make_contrib_dict(entry):
            d = {'is_org': entry['agent'].agent_type == 'org',
                 'affiliations': [a['agent'].display_name for a in
                                  entry['agent'].package_affiliations(pkg_dict['id'])]}
            if entry['agent'].agent_type == 'person':
                d['family_name'] = entry['agent'].family_name
                d['given_name'] = entry['agent'].given_names
            else:
                d['full_name'] = entry['agent'].name
            if entry['agent'].external_id and entry['agent'].external_id_scheme:
                scheme = entry['agent'].external_id_scheme
                scheme_label = id_schemes.get(scheme, {}).get('label', scheme)
                scheme_uri = id_schemes.get(scheme, {}).get('scheme_uri')
                d['identifiers'] = [{'identifier': entry['agent'].external_id_url,
                                     'scheme': scheme_label,
                                     'scheme_uri': scheme_uri}]
            return d

        creators = []
        for c in all_contributors['cited']:
            creator_dict = _make_contrib_dict(c)
            creators.append(creator_dict)

        if len(creators) == 0:
            default_author = toolkit.config.get('ckanext.doi.publisher',
                                                toolkit.config.get('ckan.site_title', 'Anonymous'))
            creators.append({'full_name': default_author,
                             'is_org': True})

        contributors = []
        for c in all_contributors['uncited']:
            # Only one type can be sent to datacite, so use the datacite role/activity where the
            # contributor is ranked highest, e.g. if they're 2nd Editor and 1st DataManager,
            # DataManager is used. If none are ranked (or there are multiple with the same rank),
            # use the first alphabetically. If there are no datacite roles/activities for this
            # contributor, use 'Other' (because contributor type is a required field).
            contrib_dict = _make_contrib_dict(c)
            datacite_roles = sorted([a for a in c['contributions'] if a.scheme == 'datacite'],
                                    key=lambda x: (x.order or len(c['contributions']), x.activity))
            if datacite_roles:
                contrib_dict['contributor_type'] = datacite_roles[0].activity
            else:
                contrib_dict['contributor_type'] = 'Other'
            contributors.append(contrib_dict)

        metadata_dict['creators'] = creators
        metadata_dict['contributors'] = contributors

        return metadata_dict, errors
