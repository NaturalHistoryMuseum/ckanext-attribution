#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from setuptools import find_packages, setup

__version__ = '1.0.0'

with open('README.md', 'r') as f:
    __long_description__ = f.read()

setup(
    name='ckanext-attribution',
    version=__version__,
    description='A CKAN extension that adds support for complex attribution.',
    long_description=__long_description__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='CKAN data attribution',
    author='Natural History Museum',
    author_email='data@nhm.ac.uk',
    url='https://github.com/NaturalHistoryMuseum/ckanext-attribution',
    license='GNU GPLv3',
    packages=find_packages(exclude=['tests']),
    namespace_packages=['ckanext', 'ckanext.attribution'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'orcid',
        'sqlalchemy',
        'requests',
        'beautifulsoup4>=4.4.0',
        'numpy',
        'spacy[transformers]',
        'unidecode',
        'nameparser',
        'prompt_toolkit',
        'fuzzywuzzy[speedup]'
    ],
    entry_points= \
        '''
        [ckan.plugins]
            attribution=ckanext.attribution.plugin:AttributionPlugin
        ''',
    )
