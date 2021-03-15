#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools

from ckan.model import Package, package_table

from ._base import BaseQuery
from .package_contribution_activity import PackageContributionActivityQuery


class PackageQuery(BaseQuery):
    ''' '''
    m = Package
    t = package_table

    @classmethod
    def get_contributions(cls, pkg_id):
        link_records = PackageContributionActivityQuery.read_package(pkg_id)
        activities = sorted([r.contribution_activity for r in link_records],
                            key=lambda x: x.activity)
        grouped_activities = {}
        for k, v in itertools.groupby(activities, key=lambda x: x.activity):
            v = list(v)  # this is necessary so we can iterate over the group twice
            ordered_agents = sorted([a for a in v if a.order is not None], key=lambda a: a.order)
            unordered_agents = sorted([a for a in v if a.order is None],
                                      key=lambda a: a.agent.sort_name)
            grouped_activities[k] = [a for a in ordered_agents] + [a for a in unordered_agents]
        return grouped_activities
