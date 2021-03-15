#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit


@toolkit.auth_allow_anonymous_access
def agent_affiliation_show(context, data_dict):
    '''
    Allow for everyone.
    '''
    return {
        'success': True
    }


@toolkit.auth_allow_anonymous_access
def agent_show(context, data_dict):
    '''
    Allow for everyone.
    '''
    return {
        'success': True
    }


@toolkit.auth_allow_anonymous_access
def agent_contribution_activity_show(context, data_dict):
    '''
    Allow for everyone.
    '''
    return {
        'success': True
    }


@toolkit.auth_allow_anonymous_access
def contribution_activity_show(context, data_dict):
    '''
    Allow for everyone.
    '''
    return {
        'success': True
    }


@toolkit.auth_allow_anonymous_access
def package_contribution_activity_show(context, data_dict):
    '''
    Allow for everyone.
    '''
    return {
        'success': True
    }

@toolkit.auth_allow_anonymous_access
def package_contributions_show(context, data_dict):
    '''
    Allow for everyone.
    '''
    return {
        'success': True
    }
