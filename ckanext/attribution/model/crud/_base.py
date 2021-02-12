#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from abc import ABCMeta
from ckan.model import DomainObject, Session
from sqlalchemy import Table
from ckan.plugins import toolkit


class BaseQuery(object):
    '''A base class for easy CRUD (create, read, update, delete) access to attribution models.'''
    __metaclass__ = ABCMeta

    #: :type: The associated database model type.
    m = DomainObject

    #: :sqlalchemy.Table: The associated database table instance
    t = Table()

    @classmethod
    def _columns(cls, **kwargs):
        '''


        :param kwargs:

        '''
        return {c.name: kwargs.get(c.name) for c in cls.t.c if c.name in kwargs}

    @classmethod
    def validate(cls, data_dict):
        '''
        Ensure the data_dict provided contains the correct parameters for creating or updating a
        record.

        :param data_dict: a complete dictionary of parameters that will be passed to :func:`create`
                          or :func:`update`
        :type data_dict: dict
        :returns: True if valid, raises error if not
        '''
        return True

    @classmethod
    def create(cls, **kwargs):
        '''
        Create a new record of type :class:`~m`.
        '''
        item_dict = cls._columns(**kwargs)
        new_item = cls.m(**item_dict)
        Session.add(new_item)
        Session.commit()
        return new_item

    @classmethod
    def read(cls, item_id):
        '''
        Retrieve a record of type :class:`~m` by its ID.

        :param item_id: the ID of the record.
        :type item_id: str
        '''
        retrieved_item = Session.query(cls.m).get(item_id)
        if retrieved_item is None:
            raise toolkit.ObjectNotFound('{0} was not found.'.format(item_id))
        return retrieved_item

    @classmethod
    def search(cls, query):
        '''
        Retrieve all records matching the search criteria.

        :param query:
        '''
        return Session.query(cls.m).filter(query).all()

    @classmethod
    def update(cls, item_id, **kwargs):
        '''


        :param item_id:
        :param kwargs:

        '''
        retrieved_item = Session.query(cls.m).filter(cls.m.id == item_id)
        if retrieved_item.count() < 1:
            raise toolkit.ObjectNotFound('{0} was not found.'.format(item_id))
        retrieved_item.update(
            cls._columns(**kwargs))
        Session.commit()
        return Session.query(cls.m).get(item_id)

    @classmethod
    def delete(cls, item_id):
        '''


        :param item_id:

        '''
        to_delete = Session.query(cls.m).get(item_id)
        if to_delete is not None:
            Session.delete(to_delete)
            Session.commit()
