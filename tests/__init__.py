from __future__ import with_statement

from flask import Flask, Response, abort, redirect, url_for, \
    jsonify, render_template

from flask_testing import TestCase, TwillTestCase, \
    ContextVariableDoesNotExist, Twill


def create_app():

    app = Flask(__name__)
    
    @app.route("/")
    def index():
        return Response("OK")

    @app.route("/template/")
    def index_with_template():
        return render_template("index.html", name="test")

    @app.route("/oops/")
    def bad_url():
        abort(404)

    @app.route("/redirect/")
    def redirect_to_index():
        return redirect(url_for("index"))

    @app.route("/ajax/")
    def ajax():
        return jsonify(name="test")

    @app.route("/forbidden/")
    def forbidden():
        abort(403)
    
    @app.route("/unauthorized/")
    def unauthorized():
        abort(401)


    return app


class TestSetup(TestCase):

    def create_app(self):
        return create_app()

    def test_setup(self):

        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


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


class TestClientUtils(TestCase):

    def create_app(self):
        return create_app()
    
    def test_get_json(self):
        response = self.client.get("/ajax/")
        self.assertEqual(response.json, dict(name="test"))

    def test_assert_200(self):
        self.assert200(self.client.get("/"))

    def test_assert_404(self):
        self.assert404(self.client.get("/oops/"))

    def test_assert_403(self):
        self.assert403(self.client.get("/forbidden/"))
    
    def test_assert_401(self):
        self.assert401(self.client.get("/unauthorized/"))

    def test_assert_405(self):
        self.assert405(self.client.post("/"))

    def test_assert_redirects(self):
        response = self.client.get("/redirect/")
        self.assertRedirects(response, "/")

    def test_assert_template_used(self):
        try:
            response = self.client.get("/template/")
            self.assert_template_used("index.html")
        except RuntimeError:
            pass

    def test_assert_template_not_used(self):
        response = self.client.get("/")
        try:
            self.assert_template_used("index.html")
            assert False
        except AssertionError:
            pass
        except RuntimeError:
            pass

    def test_get_context_variable(self):
        try:
            response = self.client.get("/template/")
            self.assertEqual(self.get_context_variable("name"), "test")
        except RuntimeError:
            pass

    def test_assert_context(self):
        try:
            response = self.client.get("/template/")
            self.assert_context("name", "test")
        except RuntimeError:
            pass

    def test_assert_bad_context(self):
        try:
            response = self.client.get("/template/")
            self.assertRaises(AssertionError, self.assert_context,
                              "name", "foo")
            self.assertRaises(AssertionError, self.assert_context,
                              "foo", "foo")
        except RuntimeError:
            pass

    def test_assert_get_context_variable_not_exists(self):
        try:
            response = self.client.get("/template/")
            self.assertRaises(ContextVariableDoesNotExist, 
                              self.get_context_variable, "foo")
        except RuntimeError:
            pass

 
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
