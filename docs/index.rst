flask-testing
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

If you are using **virtualenv**, it is assumed that you are installing flask-testing
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

    .. method:: assert200(response)
        
        Checks if ``response.status_code`` == 200

        :param response: Response returned from test client

    .. method:: assert404(response)
        
        Checks if ``response.status_code`` == 404

        :param response: Response returned from test client

    .. method:: getJSON(response)

        Returns Pythonized data from Response if JSON

        :param response: Response returned from test client

    .. method:: assertJSON(response, name, value)

        If JSON returned in dict format, checks if ``name`` in dict and 
        that ``name`` equals ``value``.
        
        :param response: Response returned from test client
        :param name: name in dict
        :param value: value of dict[name]

.. _Flask: http://flask.pocoo.org
.. _Bitbucket: http://bitbucket.org/danjac/flask-testing
