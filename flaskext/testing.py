# -*- coding: utf-8 -*-
"""
    flaskext.unit
    ~~~~~~~~~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
import unittest
import twill
import simplejson

from werkzeug import cached_property

__all__ = ["TestCase"]

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
        self._pre_setup()
        super(TestCase, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):
        self.app = self.create_app()

        self._orig_response_class = self.app.response_class
        self.app.response_class = _make_test_response(self.app.response_class)

        self.client = self.app.test_client()
       
        # now you can use flask thread locals

        self._ctx = self.app.test_request_context()
        self._ctx.push()

        self.twill_enabled = self.app.config.get('TWILL_ENABLED', False)

        if self.twill_enabled:
            self.twill_host = self.app.config.get('TWILL_HOST', '127.0.0.1')
            self.twill_port = self.app.config.get('TWILL_PORT', 5000)
            self.twill_scheme = self.app.config.get('TWILL_SCHEME' , 'http://')
            
            twill.add_wsgi_intercept(self.twill_host, 
                                     self.twill_port, 
                                     lambda: self.app)

    def _post_tearDown(self):
        
        if self.twill_enabled:
            twill.remove_wsgi_intercept(self.twill_host, 
                                        self.twill_port)

        self._ctx.pop()

        self.app.response_class = self._orig_response_class

    def twill_url(self, url):
        return "%s%s:%d%s" % (self.twill_scheme,
                              self.twill_host, 
                              self.twill_port,
                              url)

    def execute_twill_script(self, script, initial_url="/"):
        with open(script) as fp:
            self.execute_twill_string(fp.read(), initial_url)

    def execute_twill_string(self, string, initial_url="/"):
        twill.execute_string(string, initial_url=self.twill_url(initial_url))

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

