#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-dataset-contributors
# Created by the Natural History Museum in London, UK

import click
from ckan.plugins import toolkit
from ckanext.attribution.model.crud import AgentQuery


def get_commands():
    return [attribution]


@click.group()
def attribution():
    '''
    Commands for the ckanext-attribution plugin.
    '''
    pass


@attribution.command()
@click.argument('ids', nargs=-1)
def sync(ids):
    agent_external_update = toolkit.get_action('agent_external_update')
    if not ids:
        ids = [a.id for a in AgentQuery.all() if a.external_id]
    click.echo('Attempting to sync {0} records.'.format(len(ids)))
    errors = []
    with click.progressbar(ids) as bar:
        for _id in bar:
            try:
                agent_external_update({'ignore_auth': True}, {'id': _id})
            except Exception as e:
                errors.append('Error ({0}): {1}'.format(_id, e))
    failed = len(errors)
    total = len(ids)
    click.echo('Updated {0}/{1} ({2} failed)'.format(total-failed, total, failed))
    for e in errors:
        click.echo(e, err=True)

