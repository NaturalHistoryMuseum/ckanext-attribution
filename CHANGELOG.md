# Changelog

## v1.2.14 (2025-06-09)

### Build System(s)

- add ruff lint select rules Ignore does not work without select.
- remove pylint, add ruff lint ignore rules
- update ckantools

### CI System(s)

- set ruff target py version, add more ignores - avoid using fixes that don't work for python 3.8 (our current version) - ignore recommended ruff formatter conflicts - ignore more docstring rules
- update pre-commit repo versions

## v1.2.13 (2024-11-04)

### Docs

- use variable logo based on colour scheme
- fix agent table
- fix tests badge

### CI System(s)

- fix python setup action version
- add merge to valid commit types

## v1.2.12 (2024-11-04)

### Fix

- make additional cli packages optional

### Docs

- fill some empty parameters
- return -> returns
- add notes about optional CLI packages

### Style

- automatic reformat auto reformat with ruff/docformatter/prettier after config changes

### Build System(s)

- pin package versions and make cli dependencies optional
- remove version from docker compose file version specifier is deprecated

### CI System(s)

- add tomli as docformatter dep
- pull docformatter args from pyproject
- add docformatter args back
- only apply auto-fixes in pre-commit F401 returns linting errors as well as auto-fixes, so this disables the errors and just applies the fixes
- remove python version specifier
- update tool config update pre-commit repo versions and switch black to ruff
- add pull request validation workflow new workflow to check commit format and code style against pre-commit config
- update workflow files standardise format, change name of tests file

### Chores/Misc

- standardise quotes in pre-commit config
- add pull request template
- update tool details in contributing guide

## v1.2.11 (2024-08-20)

## v1.2.10 (2024-01-15)

### Fix

- add default value for q

### Chores/Misc

- add build section to read the docs config
- add regex for version line in citation file
- add citation.cff to list of files with version
- add contributing guidelines
- add code of conduct
- add citation file
- update support.md links

## v1.2.9 (2023-07-17)

### Docs

- update logos

## v1.2.8 (2023-04-11)

### Build System(s)

- fix postgres not loading when running tests in docker

### Chores/Misc

- add action to sync branches when commits are pushed to main

## v1.2.7 (2023-02-20)

### Docs

- fix api docs generation script

### Style

- reformat with prettier

### Chores/Misc

- small fixes to align with other extensions

## v1.2.6 (2023-01-31)

### Docs

- **readme**: change logo url from blob to raw

## v1.2.5 (2023-01-31)

### Docs

- **readme**: direct link to logo in readme
- **readme**: fix github actions badge

## v1.2.4 (2023-01-30)

### Build System(s)

- **docker**: use 'latest' tag for test docker image

## v1.2.3 (2022-12-12)

### Fix

- **agent.py**: add guard in case contribution activities relationship's package is None

### Docs

- **readme**: add lessc installation step

### Style

- change setup.py to single quotes

### Build System(s)

- remove less, move package.json to theme
- add package data

### Chores/Misc

- **agent.py**: add doc string to function instead of empty docstring

## v1.2.2 (2022-12-01)

### Docs

- **readme**: fix table borders
- **readme**: format test section
- **readme**: update ckan patch version in header badge
- **readme**: update installation steps

## v1.2.1 (2022-11-28)

### Fix

- enable anon access for agent_affiliations
- ignore missing limit and offset in package_contributions_show
- remove prepopulated context from get_action calls

### Chores/Misc

- set changelog generation to incremental

## v1.2.0 (2022-11-24)

### Fix

- move cli dependencies into main dependencies
- add missing packages

### Docs

- fix markdown-include references
- add section delimiters and include sections in docs

### Style

- apply formatting

### Build System(s)

- pin minor version of ckantools
- add include-markdown plugin to mkdocs

### CI System(s)

- add cz_nhm dependency in bump workflow
- **commitizen**: fix message template
- add pypi release action

### Chores/Misc

- use cz_nhm commitizen config
- improve commitizen message template
- **package.json**: fix license
- standardise package.json
- standardise package files

## v1.1.6 (2022-10-17)

## v1.1.5 (2022-09-20)

## v1.1.4 (2022-07-04)

## v1.1.3 (2022-04-11)

## v1.1.2 (2022-03-21)

## v1.1.1 (2022-03-21)

## v1.1.0 (2022-03-14)

## v1.0.2 (2022-02-28)

## v1.0.1 (2021-06-01)

## v1.0.0 (2021-05-18)
