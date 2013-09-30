from flask import Flask, Response, abort, redirect, jsonify, render_template,\
    url_for


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

    @app.route("/internal_server_error/")
    def internal_server_error():
        abort(500)

    return app
