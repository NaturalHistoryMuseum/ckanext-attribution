#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.authz import is_sysadmin
from ckantools.decorators import auth
from ckantools.vars import auth_valid


@auth()
def agent_affiliation_update(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid


@auth()
def agent_update(context, data_dict):
    """
    Only allow for sysadmins (who usually skip this method, except in tests).
    """
    return {'success': is_sysadmin(context.get('user'))}


@auth()
def agent_external_update(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid


@auth()
def contribution_activity_update(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid
