#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools
import re

import click
from ckanext.attribution.lib.orcid_api import OrcidApi
from ckanext.attribution.lib.ror_api import RorApi
from fuzzywuzzy import process
from unidecode import unidecode

from .common import multi_choice


class Combiner(object):
    def __init__(self, parser):
        self.contributors = parser.contributors
        self.affiliations = parser.affiliations
        self.api = {'ORCID': OrcidApi(),
                    'ROR': RorApi()}

    def separate(self, group):
        all_names = sorted(list(set([str(x.name) for x in group])), key=lambda x: -len(x))
        if len(all_names) > 1:
            same = click.confirm(
                'Are these all the same contributor?\n\t{0}\n'.format('\n\t'.join(all_names)),
                default=True)
            if not same:
                subgroups = {}
                for n in all_names:
                    v = [x for x in group if x.name == n]
                    if len(subgroups) == 0:
                        subgroups[n] = v
                        continue
                    matches = [m[0] for m in process.extract(n, list(subgroups.keys()))]
                    ix = multi_choice('Is "{0}" the same as any of these contributors?'.format(n),
                                      matches + [
                                          'None of these'], default=len(matches))
                    k = matches[ix] if ix < len(matches) else n
                    subgroups[k] = subgroups.get(k, []) + v
                return list(subgroups.values())
        return [group]

    def combine(self, group, name_func=None, api_func=None):
        all_names = [x.name for x in group]
        _contrib_dicts = sorted([(ct, pkgs) for c in group for ct, pkgs in c.packages.items()],
                                key=lambda x: x[0])
        _grouped_contribs = itertools.groupby(_contrib_dicts, key=lambda x: x[0])
        contrib = {
            'all_names': [str(n) for n in all_names],
            'affiliations': list(set([a for x in group for a in x.affiliations])),
            'packages': {contrib_type: list(set([pkgid for ct, pkgid in v])) for contrib_type, v in
                         _grouped_contribs},
        }
        if name_func is None:
            longest_name = sorted(list(set(all_names)), key=lambda x: -len(x))[0].strip()
            name = {'name': longest_name,
                    'key': longest_name}
        else:
            name = name_func(all_names)
        contrib.update(name)
        if api_func is not None:
            from_api = api_func(contrib)
            if from_api is not None:
                contrib.update(from_api)
        return contrib

    def combine_person_names(self, names):
        '''
        :return:
        '''

        def _filter_diacritics(name_list):
            filtered = [n for n in name_list if unidecode(n) != n]
            if len(filtered) > 0:
                return filtered
            else:
                return name_list

        given = []
        family = []
        for n in names:
            given.append(' '.join([n.first, n.middle]))
            family.append(n.last)
        given = list(set(given))
        family = list(set(family))

        # use longest family name
        family_name = sorted(_filter_diacritics(family), key=lambda x: -len(x))[0].strip()
        # given names are more complicated
        # remove empty strings and split into parts
        given = [re.split('\s+', m) for m in list(set(given)) if m != '']
        given_parts = {}
        for m in given:
            for i, x in enumerate(m):
                given_parts[i] = given_parts.get(i, []) + [x]
        given_names = ' '.join(
            [sorted(_filter_diacritics(p), key=lambda x: -len(x))[0] for p in
             given_parts.values()]).strip()
        combined = {
            'family_name': family_name,
            'given_names': given_names,
            'key': f'{family_name}, {given_names}'
        }
        return combined

    def _search_api(self, contrib, lookup_name, api_name, result_format):
        aff = '; '.join(contrib['affiliations'])
        api = self.api[api_name]
        try:
            question = f'Do any of these {api_name} results match "{lookup_name}" ({aff})?'
            click.echo(f'Searching {api_name} for "{lookup_name}"...')
            results = api.search(q=lookup_name).get(u'records', [])
            if len(results) > 0:
                i = multi_choice(question,
                                 [result_format.format(**r) for r in results] + ['None of these'],
                                 default=len(results))
                if i == len(results):
                    return
                return results[i]
            else:
                click.echo(f'No results found for "{lookup_name}".')
        except Exception as e:
            click.echo(f'{api_name} search error for "{lookup_name}"', err=True)
            click.echo(e, err=True)

    def search_orcid(self, contrib):
        display_name = ' '.join([contrib['given_names'], contrib['family_name']])
        result_format = '{family_name}, {given_names} ({external_id})'
        return self._search_api(contrib, display_name, 'ORCID', result_format)

    def search_ror(self, contrib):
        lookup_name = contrib['name']
        result_format = '{name}, {location} ({external_id})'
        return self._search_api(contrib, lookup_name, 'ROR', result_format)

    def update_affiliations(self, contributor):
        no_affiliations = len(contributor.get('affiliations', [])) == 0
        is_not_affiliation = len(contributor['packages'].get('affiliations', [])) == 0
        if no_affiliations and is_not_affiliation:
            return
        all_packages = [pkg_id for x in contributor['packages'].values() for pkg_id in x]
        for pkg in all_packages:
            items = self.affiliations.get(pkg[0])
            if items is None:
                continue
            updated_items = []
            for name, affiliation in items:
                if name in contributor['all_names']:
                    updated_items.append((contributor['key'], affiliation))
                elif affiliation in contributor['all_names']:
                    updated_items.append((name, contributor['key']))
                else:
                    updated_items.append((name, affiliation))
            self.affiliations[pkg[0]] = updated_items

    def run(self):
        combined = {'person': [],
                    'org': [],
                    'other': []}

        for g in [grp for family_name, initials_list in self.contributors['person'].items() for
                  initial, grp in initials_list.items()]:
            for person in self.separate(g):
                c = self.combine(person, self.combine_person_names, self.search_orcid)
                if c is not None:
                    combined['person'].append(c)
                    self.update_affiliations(c)
        for abbr, g in self.contributors['org'].items():
            for org in self.separate(g):
                c = self.combine(org, None, self.search_ror)
                if c is not None:
                    combined['org'].append(c)
                    self.update_affiliations(c)
        for abbr, g in self.contributors['other'].items():
            for o in self.separate(g):
                c = self.combine(o)
                if c is not None:
                    combined['other'].append(c)
                    self.update_affiliations(c)
        return combined
