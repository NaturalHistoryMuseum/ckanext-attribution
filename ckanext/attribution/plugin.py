#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import SingletonPlugin, implements, interfaces, toolkit
from ckanext.attribution.model import (relationships, agent_contribution_activity, agent,
                                       agent_affiliation, contribution_activity,
                                       package_contribution_activity)

from ckan.plugins import SingletonPlugin, implements, interfaces, toolkit
from ckanext.attribution.model import (agent, agent_affiliation, agent_contribution_activity,
                                       contribution_activity, package_contribution_activity,
                                       relationships)
from ckanext.attribution.lib import helpers
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
        from ckanext.attribution.logic.actions import create, show, update
        actions = {
            'agent_affiliation_create': create.agent_affiliation_create,
            'agent_create': create.agent_create,
            'contribution_activity_create': create.contribution_activity_create,
            'agent_affiliation_show': show.agent_affiliation_show,
            'agent_show': show.agent_show,
            'agent_contribution_activity_show': show.agent_contribution_activity_show,
            'contribution_activity_show': show.contribution_activity_show,
            'package_contribution_activity_show': show.package_contribution_activity_show,
            'agent_affiliation_update': update.agent_affiliation_update,
            'agent_update': update.agent_update,
            'contribution_activity_update': update.contribution_activity_update,
        }
        return actions

    # IAuthFunctions
    def get_auth_functions(self):
        from ckanext.attribution.logic.auth import create, show, update
        auth = {
            'agent_affiliation_create': create.agent_affiliation_create,
            'agent_create': create.agent_create,
            'contribution_activity_create': create.contribution_activity_create,
            'agent_affiliation_show': show.agent_affiliation_show,
            'agent_show': show.agent_show,
            'agent_contribution_activity_show': show.agent_contribution_activity_show,
            'contribution_activity_show': show.contribution_activity_show,
            'package_contribution_activity_show': show.package_contribution_activity_show,
            'agent_affiliation_update': update.agent_affiliation_update,
            'agent_update': update.agent_update,
            'contribution_activity_update': update.contribution_activity_update,
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
        toolkit.add_template_directory(config, u'theme/templates')
        toolkit.add_resource(u'theme/fanstatic', u'ckanext-attribution')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            u'get_agents': helpers.get_agents,
            u'can_edit': helpers.can_edit
        }