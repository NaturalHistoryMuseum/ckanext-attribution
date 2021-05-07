#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import re
from types import SimpleNamespace

import click


def multi_choice(question, options, default=0):
    click.echo('\n' + question)
    for i, o in enumerate(options):
        click.echo('\t({0}) {1}'.format(i + 1, o))
    answer = click.prompt('Choose an option', default=default + 1)
    try:
        answer = int(answer)
        click.echo('')
        return answer - 1
    except:
        click.echo('That wasn\'t an option.', err=True)
        return multi_choice(question, options, default)


rgx = SimpleNamespace(
    opening=re.compile('\('),
    closing=re.compile('\)'),
    initials=re.compile('([A-Z])\.\s*'),
    name=re.compile('(?:(?:,\s?)|^|and )([A-Za-z]+, [^,(]+)'),
    has_affiliation=re.compile('^([^()]+)\((.+)\)$'),
    no_affiliation=re.compile('^([^(),;]+)$'),
    initialism=re.compile('^[A-Z.]+$'),
    abbr=re.compile('([A-Z]|(?<=[^A-Za-z])[a-z])')
)
