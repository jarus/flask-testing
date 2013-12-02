# -*- coding: utf-8 -*-
"""
    flask_testing.utils
    ~~~~~~~~~~~~~~~~~~~

    Flask unittest integration.

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, with_statement

import gc
import time
import unittest
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import threading
from werkzeug import cached_property

# Use Flask's preferred JSON module so that our runtime behavior matches.
from flask import json_available, templating, template_rendered
if json_available:
    from flask import json

# we'll use signals for template-related tests if
# available in this version of Flask
try:
    import blinker
    _is_signals = True
except ImportError:  # pragma: no cover
    _is_signals = False

__all__ = ["TestCase"]


class ContextVariableDoesNotExist(Exception):
    pass


class JsonResponseMixin(object):
    """
    Mixin with testing helper methods
    """
    @cached_property
    def json(self):
        if not json_available:  # pragma: no cover
            raise NotImplementedError
        return json.loads(self.data)


def _make_test_response(response_class):
    class TestResponse(response_class, JsonResponseMixin):
        pass

    return TestResponse


def _empty_render(template, context, app):
    """
    Used to monkey patch the render_template flask method when
    the render_templates property is set to False in the TestCase
    """
    if _is_signals:
        template_rendered.send(app, template=template, context=context)

    return ""


class TestCase(unittest.TestCase):
    def create_app(self):
        """
        Create your Flask app here, with any
        configuration you need.
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

        self._ctx = self.app.test_request_context()
        self._ctx.push()

        if self._is_not_render_templates():
            self._monkey_patch_render_template()

        self.templates = []
        if _is_signals:
            template_rendered.connect(self._add_template)

    def _add_template(self, app, template, context):
        if len(self.templates) > 0:
            self.templates = []
        self.templates.append((template, context))

    def _post_teardown(self):
        if self._ctx is not None:
            self._ctx.pop()
        if self.app is not None:
            self.app.response_class = self._orig_response_class
        if _is_signals:
            template_rendered.disconnect(self._add_template)
        if hasattr(self, '_true_render'):
            templating._render = self._true_render

        del self.app
        del self.client
        del self.templates
        del self._ctx

        gc.collect()

    def _is_not_render_templates(self):
        return hasattr(self, 'render_templates') and not self.render_templates

    def _monkey_patch_render_template(self):
        self._true_render = templating._render
        templating._render = _empty_render

    def assertTemplateUsed(self, name, tmpl_name_attribute='name'):
        """
        Checks if a given template is used in the request.
        Only works if your version of Flask has signals
        support (0.6+) and blinker is installed.
        If the template engine used is not Jinja2, provide
        :param tmpl_name_attribute: with a value of its `Template`
        class attribute name which contains the provided :param name: value.

        :versionadded: 0.2
        :param name: template name
        :param tmpl_name_attribute: template engine specific attribute name
        """
        if not _is_signals:
            raise RuntimeError("Signals not supported")

        for template, context in self.templates:
            if getattr(template, tmpl_name_attribute) == name:
                return True
        raise AssertionError("template %s not used" % name)

    assert_template_used = assertTemplateUsed

    def get_context_variable(self, name):
        """
        Returns a variable from the context passed to the
        template. Only works if your version of Flask
        has signals support (0.6+) and blinker is installed.

        Raises a ContextVariableDoesNotExist exception if does
        not exist in context.

        :versionadded: 0.2
        :param name: name of variable
        """
        if not _is_signals:
            raise RuntimeError("Signals not supported")

        for template, context in self.templates:
            if name in context:
                return context[name]
        raise ContextVariableDoesNotExist

    def assertContext(self, name, value):
        """
        Checks if given name exists in the template context
        and equals the given value.

        :versionadded: 0.2
        :param name: name of context variable
        :param value: value to check against
        """

        try:
            self.assertEqual(self.get_context_variable(name), value)
        except ContextVariableDoesNotExist:
            self.fail("Context variable does not exist: %s" % name)

    assert_context = assertContext

    def assertRedirects(self, response, location):
        """
        Checks if response is an HTTP redirect to the
        given location.

        :param response: Flask response
        :param location: relative URL (i.e. without **http://localhost**)
        """
        self.assertTrue(response.status_code in (301, 302))
        self.assertEqual(response.location, "http://localhost" + location)

    assert_redirects = assertRedirects

    def assertStatus(self, response, status_code):
        """
        Helper method to check matching response status.

        :param response: Flask response
        :param status_code: response status code (e.g. 200)
        """
        self.assertEqual(response.status_code, status_code)

    assert_status = assertStatus

    def assert200(self, response):
        """
        Checks if response status code is 200

        :param response: Flask response
        """

        self.assertStatus(response, 200)

    assert_200 = assert200

    def assert400(self, response):
        """
        Checks if response status code is 400

        :versionadded: 0.2.5
        :param response: Flask response
        """

        self.assertStatus(response, 400)

    assert_400 = assert400

    def assert401(self, response):
        """
        Checks if response status code is 401

        :versionadded: 0.2.1
        :param response: Flask response
        """

        self.assertStatus(response, 401)

    assert_401 = assert401

    def assert403(self, response):
        """
        Checks if response status code is 403

        :versionadded: 0.2
        :param response: Flask response
        """

        self.assertStatus(response, 403)

    assert_403 = assert403

    def assert404(self, response):
        """
        Checks if response status code is 404

        :param response: Flask response
        """

        self.assertStatus(response, 404)

    assert_404 = assert404

    def assert405(self, response):
        """
        Checks if response status code is 405

        :versionadded: 0.2
        :param response: Flask response
        """

        self.assertStatus(response, 405)

    assert_405 = assert405

    def assert500(self, response):
        """
        Checks if response status code is 500

        :versionadded: 0.4.1
        :param response: Flask response
        """

        self.assertStatus(response, 500)

    assert_500 = assert500


# A LiveServerTestCase useful with Selenium or headless browsers
# Inspired by https://docs.djangoproject.com/en/dev/topics/testing/#django.test.LiveServerTestCase

class LiveServerTestCase(unittest.TestCase):

    def create_app(self):
        """
        Create your Flask app here, with any
        configuration you need.
        """
        raise NotImplementedError

    def __call__(self, result=None):
        """
        Does the required setup, doing it here
        means you don't have to call super.setUp
        in subclasses.
        """
        try:
            self._pre_setup_live()
            super(LiveServerTestCase, self).__call__(result)
        finally:
            self._post_teardown_live()

    def get_server_url(self):
        """
        Return the url of the test server
        """
        return 'http://localhost:%s' % self.port

    def _pre_setup_live(self):

        # Get the app
        self.app = self.create_app()

        if 'LIVESERVER_PORT' in self.app.config:
            self.port = self.app.config['LIVESERVER_PORT']
        else:
            # find next free port
            import socket
            sock = socket.socket()
            sock.bind(('localhost',0))
            _, self.port = sock.getsockname()
            sock.close()

        self.http_server = HTTPServer(WSGIContainer(self.app))
        self.http_server.listen(self.port)
        self._thread = threading.Thread(
            target=IOLoop().instance().start
        )

        self._thread.start()

    def _post_teardown_live(self):
        self.http_server.stop()
        IOLoop().instance().stop()
        self._thread.join()
