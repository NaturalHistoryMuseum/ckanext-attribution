#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckantools.decorators import auth
from ckantools.vars import auth_valid
from ckan.plugins import toolkit


@auth(anon=True)
def agent_affiliation_show(context, data_dict):
    """
    Allow for everyone.
    """
    return auth_valid


@auth(anon=True)
def agent_show(context, data_dict):
    """
    Allow for everyone.
    """
    return auth_valid


@auth(proxy='agent_show', anon=True)
def agent_list(context, data_dict):
    return auth_valid


@auth(anon=True)
def agent_contribution_activity_show(context, data_dict):
    """
    Allow for everyone.
    """
    return auth_valid


@auth(anon=True)
def contribution_activity_show(context, data_dict):
    """
    Allow for everyone.
    """
    return auth_valid


@auth(anon=True)
def package_contribution_activity_show(context, data_dict):
    """
    Allow for everyone.
    """
    return auth_valid


@auth(anon=True)
def package_contributions_show(context, data_dict):
    """
    Allow for everyone.
    """
    return auth_valid


@auth(proxy='agent_show')
def agent_affiliations(context, data_dict):
    # this one calls two other auth actions but the auth decorator can only handle one atm, so just
    # call the other one manually
    return toolkit.check_access('agent_affiliation_show', context, data_dict)
