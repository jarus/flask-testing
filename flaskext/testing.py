# -*- coding: utf-8 -*-
"""
    flaskext.unit
    ~~~~~~~~~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
import unittest
import simplejson
import twill

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
        self._ctx.pop()
        
        if self.twill_enabled:
            twill.remove_wsgi_intercept(self.twill_host, 
                                        self.twill_port)

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

    def getJSON(self, response):
        """
        Returns a JSON value from a response
        """
        
        return simplejson.loads(response.data)

    def assertJSONEquals(self, response, name, value):
        """
        If JSON dict, checks if name matches value
        """
        
        data = self.getJSON(response)
        assert name in data and data[name] == value

    def assertRedirects(self, response, location):
        assert response.status_code in (301, 302)
        assert response.location == "http://localhost" + location

    def assertStatus(self, response, status_code):
        self.assertEqual(response.status_code, status_code)

    def assert200(self, response):
        self.assertStatus(response, 200)

    def assert404(self, response):
        self.assertStatus(response, 404)
