#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.authz import is_sysadmin


def agent_affiliation_delete(context, data_dict):
    '''
    Allow for logged-in users.
    '''
    return {
        'success': True
    }


def agent_delete(context, data_dict):
    '''
    Only allow for sysadmins (who usually skip this method, except in tests).
    '''
    return {
        'success': is_sysadmin(context.get('user'))
    }


def agent_contribution_activity_delete(context, data_dict):
    '''
    Allow for logged-in users.
    '''
    return {
        'success': True
    }


def contribution_activity_delete(context, data_dict):
    '''
    Allow for logged-in users.
    '''
    return {
        'success': True
    }


def package_contribution_activity_delete(context, data_dict):
    '''
    Allow for logged-in users.
    '''
    return {
        'success': True
    }
