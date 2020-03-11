# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_service 1'] = {
    'data': {
        'allServicePages': {
            'edges': [
            ]
        }
    }
}

snapshots['test_information 1'] = {
    'data': {
        'allInformationPages': {
            'edges': [
            ]
        }
    }
}
