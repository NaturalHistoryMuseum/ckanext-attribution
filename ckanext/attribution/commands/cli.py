#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-dataset-contributors
# Created by the Natural History Museum in London, UK

import click
from ckan.model import Session
from ckan.model.package_extra import PackageExtra
from ckan.plugins import toolkit
from ckanext.attribution.commands import migration
from ckanext.attribution.model import (agent, agent_affiliation, agent_contribution_activity,
                                       contribution_activity, package_contribution_activity,
                                       relationships)
from ckanext.attribution.model.crud import AgentQuery, PackageQuery, \
    PackageContributionActivityQuery
from sqlalchemy import and_, or_


def get_commands():
    return [attribution]


@click.group()
def attribution():
    '''
    Commands for the ckanext-attribution plugin.
    '''
    pass


@attribution.command()
def initdb():
    contribution_activity.check_for_table()
    agent.check_for_table()
    agent_affiliation.check_for_table()
    agent_contribution_activity.check_for_table()
    package_contribution_activity.check_for_table()
    relationships.setup_relationships()


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
    click.echo('Updated {0}/{1} ({2} failed)'.format(total - failed, total, failed))
    for e in errors:
        click.echo(e, err=True)


@attribution.command()
def migratedb():
    click.secho(
        'Attempting to migrate contributors. It is HIGHLY recommended that you back up your '
        'database before running this.',
        fg='red')
    # click.confirm('Continue?', default=False, abort=True)
    # initdb()
    converted_packages = [r.package_id for r in PackageContributionActivityQuery.all()]
    unconverted_packages = PackageQuery.search(~PackageQuery.m.id.in_(converted_packages))
    contribution_extras = {
        p.id: Session.query(PackageExtra).filter(PackageExtra.package_id == p.id,
                                                 PackageExtra.key == 'contributors').first() for p
        in unconverted_packages}
    total = len(unconverted_packages)
    parser = migration.Parser()

    for i, pkg in enumerate(unconverted_packages):
        click.echo('Processing package {0} of {1}.\n'.format(i + 1, total))
        parser.run(pkg.author, pkg.id, 'author')
        extras = contribution_extras.get(pkg.id).value if pkg.id in contribution_extras else None
        parser.run(extras, pkg.id, 'contributor')

    combiner = migration.Combiner(parser)
    combined = combiner.run()
    agent_lookup = {}
    agent_create = toolkit.get_action('agent_create')
    contribution_activity_create = toolkit.get_action('contribution_activity_create')
    agent_affiliation_create = toolkit.get_action('agent_affiliation_create')
    remove_keys = ['packages', 'affiliations', 'key', 'all_names']
    for agent_type, agents in combined.items():
        for a in agents:
            try:
                # create the agent (check it doesn't exist first)
                agent_dict = {
                    'agent_type': agent_type,
                    **{k: v for k, v in a.items() if k not in remove_keys}
                }
                if agent_type == 'person':
                    filters = [and_(AgentQuery.m.family_name == a['family_name'],
                                    AgentQuery.m.given_names == a['given_names'])]
                else:
                    filters = [AgentQuery.m.name == a['name']]
                if a.get('external_id'):
                    filters.append(AgentQuery.m.external_id == a.get('external_id'))
                matches = AgentQuery.search(or_(*filters))
                if len(matches) == 1:
                    new_agent = matches[0].as_dict()
                elif len(matches) > 1:
                    choice_ix = migration.multi_choice(
                        f'Does "{a["key"]}" match any of these existing agents?',
                        [m.display_name for m in matches] + ['None of these'])
                    if choice_ix == len(matches):
                        del a['external_id']
                        del a['external_id_scheme']
                        new_agent = agent_create({'ignore_auth': True}, agent_dict)
                    else:
                        new_agent = matches[choice_ix].as_dict()
                else:
                    new_agent = agent_create({'ignore_auth': True}, agent_dict)
                agent_lookup[a['key']] = new_agent['id']
                # then activities
                for pkg, order in a['packages'].get('author', []):
                    # create citation
                    contribution_activity_create({'ignore_auth': True},
                                                 {'activity': '[citation]',
                                                  'scheme': 'internal',
                                                  'order': order,
                                                  'package_id': pkg,
                                                  'agent_id': new_agent['id']})
                    # then the actual activity
                    contribution_activity_create({'ignore_auth': True},
                                                 {'activity': 'Unknown',
                                                  'scheme': 'internal',
                                                  'package_id': pkg,
                                                  'agent_id': new_agent['id']})
                for pkg, _ in a['packages'].get('contributor', []):
                    # just the activity for this one
                    contribution_activity_create({'ignore_auth': True},
                                                 {'activity': 'Unknown',
                                                  'scheme': 'internal',
                                                  'package_id': pkg,
                                                  'agent_id': new_agent['id']})
            except Exception as e:
                # very broad catch just so it doesn't ruin everything if one thing breaks
                click.echo(f'Skipping {a["key"]} due to error: {e}', err=True)
    # finally, the affiliations
    for pkg, pairs in combiner.affiliations.items():
        for agent_a, agent_b in pairs:
            try:
                agent_affiliation_create({'ignore_auth': True},
                                         {'agent_a_id': agent_lookup[agent_a],
                                          'agent_b_id': agent_lookup[agent_b],
                                          'package_id': pkg})
            except Exception as e:
                # very broad catch just so it doesn't ruin everything if one thing breaks
                click.echo(f'Skipping {agent_a} + {agent_b} affiliation due to error: {e}',
                           err=True)

    # finally finally, update the package author strings
    package_show = toolkit.get_action('package_show')  # pkg.as_dict() doesn't work (:
    package_update = toolkit.get_action('package_update')
    for pkg in unconverted_packages:
        try:
            pkg_dict = package_show({}, {'id': pkg.id})
            package_update({'ignore_auth': True, 'user': None}, pkg_dict)
        except Exception as e:
            # very broad catch just so it doesn't ruin everything if one thing breaks
            click.echo(f'Skipping {pkg.id} due to error: {e}', err=True)
