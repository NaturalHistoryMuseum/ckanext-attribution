#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from collections import Counter
from dataclasses import dataclass

import click
import spacy
from nameparser import HumanName
from prompt_toolkit import prompt

from .common import rgx, multi_choice


@dataclass
class ParsedSegment:
    name: str
    text: str
    affiliations: list
    packages: dict


class Parser(object):
    '''
    Extracts names and affiliations from text.
    '''

    def __init__(self):
        self.contributors = {
            'person': {},
            'org': {},
            'other': {}
        }
        self.affiliations = {}
        spacy_model = 'en_core_web_trf'
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            spacy.cli.download(spacy_model)
            self.nlp = spacy.load(spacy_model)

    def run(self, txt, pkg_id, contrib_type):
        '''
        Run the whole process over a line of text.
        :param txt: the chunk of text to process
        :param pkg_id: associated package
        :param contrib_type: author, contributor, or affiliation
        :return: list of ParsedSegment instances extracted from the text
        '''
        if not self.validate(txt):
            return
        segments = []
        for line in txt.split('\n'):
            line = line.replace('\\r', '')
            sublines = self.split(line)
            for i, subline in enumerate(sublines):
                if subline == '':
                    continue
                if contrib_type != 'affiliation':
                    name, affiliations = self.extract_affiliations(subline)
                    for a in affiliations:
                        self.affiliations[pkg_id] = self.affiliations.get(pkg_id, []) + [
                            (name.strip(), a)]
                        parsed_affiliation = ParsedSegment(a.strip(), text=a, affiliations=[],
                                                           packages={'affiliation': (pkg_id, None)})
                        self.sort_contributor(parsed_affiliation)
                else:
                    name = subline
                    affiliations = []
                order = (i + 1) if contrib_type == 'author' else None
                parsed_segment = ParsedSegment(name=name.strip(), text=subline,
                                               affiliations=affiliations,
                                               packages={contrib_type: (pkg_id, order)})
                self.sort_contributor(parsed_segment)
                segments.append(parsed_segment)
        return segments

    def validate(self, txt):
        '''
        Check the text can/should actually be parsed.
        :return: True/False
        '''
        if txt is None:
            return False
        parsed = self.nlp(txt)
        # check that it has some proper nouns and doesn't just look like a sentence
        tokens = [t for t in parsed]
        pos = Counter([t.pos_ for t in tokens])
        if len(tokens) == 0:
            return []
        pc_proper_nouns = pos.get('PROPN', 0) / len(tokens)
        if pc_proper_nouns < 0.5:
            click.echo('\nThis text doesn\'t look right:')
            click.echo(txt)
            return not click.confirm('Skip it?')
        return True

    def split(self, txt):
        '''
        Uses multiple sub-methods to attempt to split the text into individual contributors.
        :param txt:
        :return:
        '''
        lines = [ln.strip() for ln in txt.split('\n')]
        segments = [rgx.initials.sub('\\1 ', s).strip() for ln in lines for s in ln.split(';')]
        names = []

        def _process_segment(segment):
            if ';' in segment:
                semicolon_splits = [s.strip() for s in segment.split(';')]
            else:
                semicolon_splits = []
            rgx_splits = rgx.name.findall(segment)
            nlp_sep_splits = self._split_by_nlp_sep(segment)
            nlp_ent_splits = self._split_by_nlp_ents(segment)
            options = []
            printable_options = []
            for o in sorted(
                [nlp_ent_splits, nlp_sep_splits, rgx_splits, semicolon_splits, [segment]],
                    key=lambda x: -len(x)):
                if len(o) == 0:
                    continue
                printable = '; '.join(o) + ' ({0} fragments)'.format(len(o))
                if printable in printable_options:
                    continue
                options.append(o)
                printable_options.append(printable)
            options.append(None)
            printable_options.append('None of these')
            if len(options) > 1:
                click.echo(segment)
                ix = multi_choice('Which one looks right?', printable_options)
                return options[ix]

        for t in segments:
            splits = None
            while not splits:
                splits = _process_segment(t)
                if splits:
                    names += splits
                else:
                    t = prompt('Edit the line (try adding ";" between contributors): ', default=t)
        return names

    def _split_by_nlp_sep(self, txt):
        '''
        Finds entities using spacy, then attempts to identify the character(s) separating them and
        splits by that.
        '''
        parsed = self.nlp(txt)
        if len(parsed.ents) > 2:
            start_char = parsed.ents[0].end_char
            end_char = parsed.ents[1].start_char
            sep = txt[start_char:end_char].strip()
            if sep == '':
                sep = '\n'
            return [s.strip() for s in txt.split(sep)]
        return [txt]

    def _split_by_nlp_ents(self, txt):
        '''
        Extract all entities from the text using spacy.
        '''
        parsed = self.nlp(txt)
        return [ent.text for ent in parsed.ents]

    def extract_affiliations(self, txt):
        '''
        Uses regexes to find probable affiliations in parentheses.
        :return: contributor name, list of affiliations
        '''
        has_affiliation = rgx.has_affiliation.match(txt)
        no_affiliation = rgx.no_affiliation.match(txt)
        if has_affiliation is not None:
            return has_affiliation.groups()[0], self.split(has_affiliation.groups()[1])
        if no_affiliation is not None:
            return no_affiliation.groups()[0], []
        else:
            return txt, []

    def sort_contributor(self, c: ParsedSegment):
        '''
        Sort a contributor into lists based on agent type.
        '''
        name = HumanName(c.name)
        _type = '?'
        if name.last in self.contributors['person']:
            _type = 'person'
        else:
            for k, v in self.contributors.items():
                if k == 'person':
                    continue
                if c.name in v:
                    _type = k
        if _type == '?':
            i = multi_choice('What type of contributor is "{0}"?'.format(c.name),
                             self.contributors.keys())
            _type = list(self.contributors.keys())[i]
        if _type == 'person':
            if name.last == '':
                name.last = name.first
                name.first = '?'
            c.name = name
            family_name_records = self.contributors[_type].get(name.last, {})
            initial_records = family_name_records.get(name.first[0], []) + [c]
            family_name_records[name.first[0]] = initial_records
            self.contributors[_type][name.last] = family_name_records
        else:
            initials = ''.join(rgx.abbr.findall(c.name))
            self.contributors[_type][initials] = self.contributors[_type].get(initials, []) + [c]
