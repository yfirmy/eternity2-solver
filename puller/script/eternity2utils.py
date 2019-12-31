#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Job Puller
#
#  Copyright © 2019 Yohan Firmy
#

from datetime import datetime

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
