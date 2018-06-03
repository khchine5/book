# -*- coding: utf-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Does not actually test anything.

You can run only these tests by issuing::

  $ python setup.py test -s tests.DemoTests.test_simple

Or::

  $ go adg
  $ python manage.py test tests.test_simple



"""

from __future__ import unicode_literals
from __future__ import print_function

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


class SimpleTests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        User = rt.models.users.User
        UserTypes = rt.models.users.UserTypes

