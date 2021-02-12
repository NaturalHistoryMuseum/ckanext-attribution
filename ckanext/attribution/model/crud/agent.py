#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import Session
from ckan.plugins import toolkit
from ckanext.attribution.lib.orcid_api import OrcidApi
from ckanext.attribution.model.agent import Agent, agent_table
from requests import HTTPError

from ._base import BaseQuery


class AgentQuery(BaseQuery):
    '''
    CRUD methods for :class:`~ckanext.attribution.model.agent.Agent`.

    Fields
    ======
    :param agent_type: broad type of agent; usually 'individual' or 'org'
    :type agent_type: str
    :param family_name: family name of an individual [individual only, required]
    :type family_name: str, optional
    :param given_names: given name(s) or initials of an individual [individual only, required]
    :type given_names: str, optional
    :param given_names_first: whether given names should be displayed before the family name
                              (default True) [individual only, optional]
    :type given_names_first: bool, optional
    :param orcid: an individual's `ORCID <https://orcid.org>`_ [individual only, optional]
    :type orcid: str, optional
    :param user_id: the ID for a registered user of this CKAN instance associated with this agent
                    [individual only, optional]
    :type user_id: str, optional
    :param name: name of an organisation [org only, required]
    :type name: str, optional
    :param ror_id: an organisation's `ROR <https://ror.org>`_ ID [org only, optional]
    :type ror_id: str, optional
    '''

    #: :type: The associated database model type.
    m = Agent

    #: :sqlalchemy.Table: The associated database table instance (agent_table).
    t = agent_table

    @classmethod
    def validate(cls, data_dict):
        valid_agent_types = ['individual', 'org']
        agent_type = toolkit.get_or_bust(data_dict, 'agent_type')
        if agent_type not in valid_agent_types:
            raise toolkit.Invalid(
                'Agent type must be one of {0}'.format(', '.join(valid_agent_types)))

        valid_params = {
            'individual': dict(required=[u'family_name', u'given_names'],
                               optional=[u'given_names_first', u'orcid', u'user_id']),
            'org': dict(required=[u'name'], optional=[u'ror_id'])
        }
        required = valid_params[agent_type]['required']
        optional = valid_params[agent_type]['optional']
        for k in required:
            if k not in data_dict:
                raise toolkit.ValidationError(u'{0} is a required field.'.format(k))
        all_fields = required + optional
        for k in data_dict:
            if k not in all_fields:
                raise toolkit.ValidationError(
                    u'{0} is not a valid field for the "{1}" agent type.'.format(k, agent_type))

    @classmethod
    def read_orcid(cls, orcid):
        '''
        Retrieve an agent record by its ORCID.

        :param orcid: the full ORCID of the agent
        :type orcid: str
        :returns: One agent or None if not found.
        :rtype: Agent

        '''
        # TODO: does this actually return None?
        return Session.query(Agent).filter(Agent.orcid == orcid).first()

    @classmethod
    def update_from_orcid_api(cls, agent_id, api=None):
        '''
        Update the data for an agent using the ORCID API and the agent's stored ORCID.

        :param agent_id: the full ID of the agent record
        :type agent_id: str
        :param api: an API instance already in use (useful if performing this action over many
                    agent records, to avoid instantiating many API connections) (Default value = None)
        :type api: OrcidApi
        :returns: the updated agent record
        :rtype: Agent

        '''
        if api is None:
            api = OrcidApi()
        current_entry = cls.read(agent_id)
        if current_entry.orcid is None:
            raise Exception(toolkit._('Record does not have an ORCID.'))
        try:
            orcid_record = api.read(current_entry.orcid)
        except HTTPError:
            orcid_results = api.search(orcid_q=current_entry.orcid)
            if orcid_results[u'num-found'] == 0:
                raise Exception(toolkit._(u'This ORCID does not exist.'))
            else:
                orcid_record = orcid_results[u'result'][0]
        updated_entry = api.as_agent_record(orcid_record)
        return cls.update(agent_id, **updated_entry)
