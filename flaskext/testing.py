# -*- coding: utf-8 -*-
"""
    flaskext.testing
    ~~~~~~~~~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
import StringIO
import unittest
import twill
import simplejson

from werkzeug import cached_property

__all__ = ["TestCase", "TwillTestCase"]

class JsonResponseMixin(object):
    """
    Mixin with testing helper methods
    """
    @cached_property
    def json(self):
        return simplejson.loads(self.data)


def _make_test_response(response_class):
    class TestResponse(response_class, JsonResponseMixin):
        pass

    return TestResponse


class TestCase(unittest.TestCase):
    
    def create_app(self):
        """
        Create your Flask app here, with any
        configuration you need
        """
        raise NotImplementedError

    def __call__(self, result=None):
        """
        Does the required setup, doing it here
        means you don't have to call super.setUp
        in subclasses.
        """
        try:
            self._pre_setup()
            super(TestCase, self).__call__(result)
        finally:
            self._post_teardown()

    def _pre_setup(self):
        self.app = self.create_app()

        self._orig_response_class = self.app.response_class
        self.app.response_class = _make_test_response(self.app.response_class)

        self.client = self.app.test_client()
       
        # now you can use flask thread locals

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_teardown(self):
        self._ctx.pop()

        self.app.response_class = self._orig_response_class

    def assertRedirects(self, response, location):
        assert response.status_code in (301, 302)
        assert response.location == "http://localhost" + location

    assert_redirects = assertRedirects

    def assertStatus(self, response, status_code):
        self.assertEqual(response.status_code, status_code)


    assert_status = assertStatus

    def assert200(self, response):

        self.assertStatus(response, 200)

    assert_200 = assert200

    def assert404(self, response):

        self.assertStatus(response, 404)

    assert_404 = assert404


class TwillTestCase(TestCase):
    """
    TestCase with Twill helper methods.
    """

    twill_host = "127.0.0.1"
    twill_port = 5000
    twill_scheme = "http"

    def _pre_setup(self):
        super(TwillTestCase, self)._pre_setup()
        twill.set_output(StringIO.StringIO())
        twill.commands.clear_cookies()
        twill.add_wsgi_intercept(self.twill_host, 
                                 self.twill_port, 
                                 lambda: self.app)
    
        self.browser = twill.get_browser()

    def _post_teardown(self):

        twill.remove_wsgi_intercept(self.twill_host, 
                                    self.twill_port)

        twill.commands.reset_output()
        
        super(TwillTestCase, self)._post_teardown()

    def make_twill_url(self, url):
        return "%s://%s:%d%s" % (self.twill_scheme,
                                 self.twill_host, 
                                 self.twill_port,
                                 url)

