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

try:
    from ckanext.doi.interfaces import IDoi

    doi_available = True
except ImportError:
    doi_available = False


class AttributionPlugin(SingletonPlugin):
    '''A CKAN extension that adds support for complex attribution.'''

    implements(interfaces.IActions, inherit=True)
    implements(interfaces.IAuthFunctions, inherit=True)
    implements(interfaces.IConfigurable)
    implements(interfaces.IConfigurer)
    implements(interfaces.ITemplateHelpers)

    # IActions
    def get_actions(self):
        from ckanext.attribution.logic.actions import create, show, update, delete, extra
        actions = {
            'agent_affiliation_create': create.agent_affiliation_create,
            'agent_create': create.agent_create,
            'contribution_activity_create': create.contribution_activity_create,
            'agent_affiliation_show': show.agent_affiliation_show,
            'agent_show': show.agent_show,
            'agent_list': show.agent_list,
            'agent_contribution_activity_show': show.agent_contribution_activity_show,
            'contribution_activity_show': show.contribution_activity_show,
            'package_contribution_activity_show': show.package_contribution_activity_show,
            'package_contributions_show': show.package_contributions_show,
            'agent_all_affiliations': show.agent_all_affiliations,
            'agent_affiliation_update': update.agent_affiliation_update,
            'agent_update': update.agent_update,
            'agent_external_update': update.agent_external_update,
            'contribution_activity_update': update.contribution_activity_update,
            'agent_affiliation_delete': delete.agent_affiliation_delete,
            'agent_delete': delete.agent_delete,
            'agent_contribution_activity_delete': delete.agent_contribution_activity_delete,
            'contribution_activity_delete': delete.contribution_activity_delete,
            'package_contribution_activity_delete': delete.package_contribution_activity_delete,
            'contribution_roles_list': extra.contribution_roles_list,
            'agent_external_search': extra.agent_external_search,
            'external_id_schemes': extra.external_id_schemes
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

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_contributions': helpers.get_contributions,
            'as_string': helpers.as_string,
            'can_edit': helpers.can_edit,
            'split_caps': helpers.split_caps
        }
