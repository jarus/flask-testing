from __future__ import with_statement

from flask_testing import TestCase, TwillTestCase, Twill
from .flask_app import create_app


class TestTwill(TestCase):

    def create_app(self):
        app = create_app()
        app.config.from_object(self)
        return app

    def test_twill_setup(self):

        twill = Twill(self.app)

        self.assertEqual(twill.host, "127.0.0.1")
        self.assertEqual(twill.port, 5000)
        self.assertTrue(twill.browser is not None)

    def test_make_twill_url(self):
        with Twill(self.app) as t:
            self.assertEqual(t.url("/"), "http://127.0.0.1:5000/")


class TestTwillDeprecated(TwillTestCase):

    def create_app(self):
        app = create_app()
        app.config.from_object(self)
        return app

    def test_twill_setup(self):
        self.assertEqual(self.twill_host, '127.0.0.1')
        self.assertEqual(self.twill_port, 5000)
        self.assertTrue(self.browser is not None)

    def test_make_twill_url(self):
        self.assertEqual(self.make_twill_url("/"), "http://127.0.0.1:5000/")
