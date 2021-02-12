<img src=".github/nhm-logo.svg" align="left" width="150px" height="100px" hspace="40"/>

# ckanext-attribution

[![Travis](https://img.shields.io/travis/NaturalHistoryMuseum/ckanext-attribution/master.svg?style=flat-square)](https://travis-ci.org/NaturalHistoryMuseum/ckanext-attribution)
[![Coveralls](https://img.shields.io/coveralls/github/NaturalHistoryMuseum/ckanext-attribution/master.svg?style=flat-square)](https://coveralls.io/github/NaturalHistoryMuseum/ckanext-attribution)
[![CKAN](https://img.shields.io/badge/ckan-2.9.1-orange.svg?style=flat-square)](https://github.com/ckan/ckan)

_A CKAN extension that adds support for complex attribution._


# Overview

This extension


# Installation

Path variables used below:
- `$INSTALL_FOLDER` (i.e. where CKAN is installed), e.g. `/usr/lib/ckan/default`
- `$CONFIG_FILE`, e.g. `/etc/ckan/default/development.ini`

1. Clone the repository into the `src` folder:

  ```bash
  cd $INSTALL_FOLDER/src
  git clone https://github.com/NaturalHistoryMuseum/ckanext-attribution.git
  ```

2. Activate the virtual env:

  ```bash
  . $INSTALL_FOLDER/bin/activate
  ```

3. Install the requirements from requirements.txt:

  ```bash
  cd $INSTALL_FOLDER/src/ckanext-attribution
  pip install -r requirements.txt
  ```

4. Run setup.py:

  ```bash
  cd $INSTALL_FOLDER/src/ckanext-attribution
  python setup.py develop
  ```

5. Add 'attribution' to the list of plugins in your `$CONFIG_FILE`:

  ```ini
  ckan.plugins = ... attribution
  ```

# Configuration

These are the options that can be specified in your .ini config file.

Name|Description|Options
--|--|--
||


# Usage



# Testing
_Test coverage is currently extremely limited._

To run the tests in this extension, there is a Docker compose configuration available in this
repository to make it easy.

To run the tests against ckan 2.9.x on Python3:

1. Build the required images
```bash
docker-compose build
```

2. Then run the tests.
   The root of the repository is mounted into the ckan container as a volume by the Docker compose
   configuration, so you should only need to rebuild the ckan image if you change the extension's
   dependencies.
```bash
docker-compose run ckan
```

The ckan image uses the Dockerfile in the `docker/` folder which is based on `openknowledge/ckan-dev:2.9-py2`
