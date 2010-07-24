from flask import Flask, Response, abort, redirect, url_for, \
    jsonify, render_template

from flaskext.testing import TestCase, TwillTestCase, \
    ContextVariableDoesNotExist

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

    return app

class TestSetup(TestCase):

    def create_app(self):
        return create_app()

    def test_setup(self):

        assert self.app
        assert self.client
        assert self._ctx

class TestTwill(TwillTestCase):
    
    def create_app(self):
        app = create_app()
        app.config.from_object(self)
        return app

    def test_twill_setup(self):
        
        assert self.twill_host == '127.0.0.1'
        assert self.twill_port == 5000

    def test_make_twill_url(self):

        assert self.make_twill_url("/") == \
            "http://127.0.0.1:5000/"

class TestClientUtils(TestCase):

    def create_app(self):
        return create_app()
    
    def test_getJSON(self):

        response = self.client.get("/ajax/")
        assert response.json == dict(name="test")

    def test_assert_200(self):

        response = self.client.get("/")
        self.assert200(response)

    def test_assert_404(self):

        response = self.client.get("/oops/")
        self.assert404(response)

    def test_assert_403(self):

        response = self.client.get("/forbidden/")
        self.assert403(response)

    def test_assert_405(self):

        response = self.client.post("/")
        self.assert405(response)

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
        except RuntimeError:
            pass

    def test_get_context_variable(self):

        try:
            response = self.client.get("/template/")
            assert self.get_context_variable("name") == "test"
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
            self.assertRaises(AssertionError, self.assert_context, "name", "foo")
            self.assertRaises(AssertionError, self.assert_context, "foo", "foo")
        except RuntimeError:
            pass

    def test_assert_get_context_variable_not_exists(self):

        try:
            response = self.client.get("/template/")
            self.assertRaises(ContextVariableDoesNotExist, 
                              self.get_context_variable, "foo")
        except RuntimeError:
            pass

    
