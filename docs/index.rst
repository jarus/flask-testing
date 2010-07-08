Flask-Testing
======================================

.. module:: flask-testing

The **Flask-Testing** extension provides unit testing utilities for Flask.

Source code and issue tracking at `Bitbucket`_.

Installing Flask-Testing
------------------------

Install with **pip** and **easy_install**::

    pip install Flask-Testing

or download the latest version from Bitbucket::

    hg clone http://bitbucket.org/danjac/flask-testing

    cd flask-testing

    python setup.py develop

If you are using **virtualenv**, it is assumed that you are installing **Flask-Testing**
in the same virtualenv as your Flask application(s).

Writing unit tests
------------------

Simply subclass the ``TestCase`` class::

    from flaskext.testing import TestCase

    class MyTest(TestCase):

        pass


You must specify the ``create_app`` method, which should return a Flask instance::

    from flaskext.testing import TestCase

    class MyTest(TestCase):

        def create_app(self):

            app = Flask(__name__)
            app.config['TESTING'] = True
            return app

If you don't define ``create_app`` a ``NotImplementedError`` will be raised.

Testing JSON responses
----------------------

If you are testing a view that returns a JSON response, you can test the output using
a special ``json`` attribute appended to the ``Response`` object::

    @app.route("/ajax/")
    def some_json():
        return jsonify(success=True)

    class TestViews(TestCase):
        def test_some_json(self):
            response = self.client.get("/ajax/")
            self.assertEquals(response.json, dict(success=True))

Using with Twill
----------------

`Twill`_ is a simple language for browing the Web through
a command line interface. You can use it in conjunction with ``TwillTestCase`` to write
functional tests for your views. 

``TwillTestCase`` is a subclass of ``TestCase``. It sets up `Twill`_ for use with your test 
cases. See the API below for details.

Testing with SQLAlchemy
-----------------------

This covers a couple of points if you are using **Flask-Testing** with `SQLAlchemy`_. It is 
assumed that you are using the `Flask-SQLAlchemy`_ extension, but if not the examples should
not be too difficult to adapt to your own particular setup.

First, ensure you set the database URI to something other than your production database ! Second,
it's usually a good idea to create and drop your tables with each test run, to ensure clean tests::

    from flaskext.testing import TestCase
    
    from myapp import create_app, db

    class MyTest(TestCase):
        
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        TESTING = True

        def create_app(self):
            
            # pass in test configuration
            return create_app(self)
        
        def setUp(self):

            db.create_all()

        def tearDown(self):

            db.session.remove()
            db.drop_all()

Notice also that ``db.session.remove()`` is called at the end of each test, to ensure the SQLAlchemy
session is properly removed and that a new session is started with each test run - this is a common
"gotcha".

Also notice that for this example the SQLite in-memory database is used : while it is faster for tests,
if you have database-specific code (e.g. for MySQL or PostgreSQL) it may not be applicable.

You may also want to add a set of instances for your database inside of a ``setUp()`` once your database
tables have been created. If you want to work with larger sets of data, look at `Fixture`_ which includes
support for SQLAlchemy.
    

API
---

.. module:: flaskext.testing

.. class:: TestCase
        
    Subclass of ``unittest.TestCase``. When run the following properties are defined:

        * ``self.app`` : Flask application defined by ``create_app``
        * ``self.client`` : Test client instance
    
    The Flask application test context is created and disposed of inside the test run.

    .. method:: create_app()
        
        Returns a Flask app instance. If not defined raises ``NotImplementedError``.
    
    .. method:: assertRedirects(response, location)
        
        Checks if HTTP response and redirect URL matches location.

        :param response: Response returned from test client
        :param location: URL (automatically prefixed by `http://localhost`)

    .. method:: assert_redirects(response)
        
        Alias of ``assertRedirects``.

    .. method:: assert200(response)
        
        Checks if ``response.status_code`` == 200

        :param response: Response returned from test client

    .. method:: assert_202(response)
        
        Alias of ``assert202``.

    .. method:: assert404(response)
        
        Checks if ``response.status_code`` == 404

        :param response: Response returned from test client

    .. method:: assert_404(response)
        
        Alias of ``assert404``.
        
.. class:: TwillTestCase(TestCase)
    
    Subclass of ``TestCase`` with additional functionality
    for managing `Twill`_. Handles WSGI intercept inside each
    test. 

    A ``browser`` instance is created with each setup, which is a `Twill`_ browser instance.

    .. attribute:: twill_scheme

        HTTP scheme used by `Twill`_ (default **http**)

    .. attribute:: twill_host

        HTTP host used by `Twill`_ (default **127.0.0.1**)

    .. attribute:: twill_port

        HTTP port used by `Twill`_ (default **5000**)

    .. method:: make_twill_url(url)

        Creates an absolute URL based on the `Twill`_ URL attributes.


.. _Flask: http://flask.pocoo.org
.. _Bitbucket: http://bitbucket.org/danjac/flask-testing
.. _Twill: http://twill.idyll.org/
.. _Fixture: http://farmdev.com/projects/fixture/index.html
.. _SQLAlchemy: http://sqlalchemy.org
.. _Flask-SQLAlchemy: http://packages.python.org/Flask-SQLAlchemy/
