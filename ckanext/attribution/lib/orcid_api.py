#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import orcid
import requests
from ckan.plugins import toolkit
from paste.deploy.converters import asbool
from werkzeug.utils import cached_property


class OrcidApi(object):
    ''' '''
    def __init__(self):
        self.key = toolkit.config.get(u'ckanext.attribution.orcid_key')
        self.secret = toolkit.config.get(u'ckanext.attribution.orcid_secret')
        self._debug = asbool(toolkit.config.get(u'ckanext.attribution.debug', True))

    @cached_property
    def conn(self):
        ''' '''
        if self.key is None or self.secret is None:
            raise Exception(toolkit._(u'ORCID API credentials not supplied.'))
        return orcid.PublicAPI(self.key, self.secret, sandbox=self._debug)

    @cached_property
    def read_token(self):
        ''' '''
        if self.key is None or self.secret is None:
            raise Exception(toolkit._(u'ORCID API credentials not supplied.'))
        url = 'https://sandbox.orcid.org/oauth/token' if self._debug else \
            'https://orcid.org/oauth/token'
        r = requests.post(url, data={
            'client_id': self.key,
            'client_secret': self.secret,
            'grant_type': 'client_credentials',
            'scope': '/read-public'
        }, headers={
            'Accept': 'application/json'
        })
        if r.ok:
            return r.json()['access_token']
        else:
            return None

    def search(self, surname_q=None, orcid_q=None, given_q=None):
        '''
        

        :param surname_q:  (Default value = None)
        :param orcid_q:  (Default value = None)
        :param given_q:  (Default value = None)

        '''
        query = []
        if surname_q is not None and surname_q != u'':
            query.append(u'family-name:' + surname_q)
        if orcid_q is not None and orcid_q != u'':
            query.append(u'orcid:' + orcid_q)
        if given_q is not None and given_q != u'':
            query.append(u'given-names:' + given_q)
        query = u'+AND+'.join(query)
        search_results = self.conn.search(query, access_token=self.read_token, rows=10)
        return search_results

    def read(self, orcid_id):
        '''
        

        :param orcid_id: 

        '''
        record = self.conn.read_record_public(orcid_id, 'record', self.read_token)
        return record

    def as_agent_record(self, orcid_record):
        '''
        

        :param orcid_record: 

        '''
        # FIXME
        names = orcid_record.get(u'person', {}).get(u'name', {})
        employments = orcid_record.get(u'activities-summary', {}).get(u'employments', {}).get(
            u'employment-summary', [])
        return {
            u'surname': names.get(u'family-name', {}).get(u'value', u''),
            u'given_names': names.get(u'given-names', {}).get(u'value', u''),
            u'affiliations': list(
                set([e.get(u'organization', {}).get(u'name', None) for e in employments if
                     e.get(u'organization', {}).get(u'name', None) is not None])),
            u'orcid': orcid_record.get(u'orcid-identifier', {}).get(u'path', u'')
        }
