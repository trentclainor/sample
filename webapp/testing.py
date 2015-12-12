# -*- coding: utf-8 -*-

"""
    testing
    ~~~~~~~

    More useful TestCase for tests.

"""

from settings import TestingConfig
from flask.ext.testing import TestCase
from webapp.models import User
from webapp.helpers import AppFactory
from webapp.extensions import db


class KitTestCase(TestCase):

    def create_app(self):
        return AppFactory(TestingConfig).get_app(__name__)

    def setUp(self):
        db.create_all()
        self.user = User(mail='john@doe.com', password='test', role='manager')
        self.user.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assertContains(self, response, text, count=None,
                       status_code=200, msg_prefix=''):
        """
        Asserts that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` occurs ``count`` times in the content of the response.
        If ``count`` is None, the count doesn't matter - the assertion is true
        if the text occurs at least once in the response.
        """

        if msg_prefix:
            msg_prefix += ": "

        self.assertEqual(response.status_code, status_code,
            msg_prefix + "Couldn't retrieve content: Response code was %d"
                         " (expected %d)" % (response.status_code, status_code))

        real_count = response.data.count(text)
        if count is not None:
            self.assertEqual(real_count, count,
                msg_prefix + "Found %d instances of '%s' in response"
                             " (expected %d)" % (real_count, text, count))
        else:
            self.assertTrue(real_count != 0,
                msg_prefix + "Couldn't find '%s' in response" % text)
