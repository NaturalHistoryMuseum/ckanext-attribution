#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK


from ckantools.decorators import auth

valid = {'success': True}


@auth(anon=True)
def attribution_controlled_lists():
    return valid


@auth('agent_show')
def agent_external_search():
    return valid


@auth('agent_show')
def agent_external_read():
    return valid


@auth(anon=True)
def validate_external_id():
    return valid
