"""
Flask-Testing
-------------

Flask unittest integration.

Links
`````

* `documentation <http://packages.python.org/Flask-Testing>`_
* `development version <http://github.com/jarus/flask-testing/zipball/master#egg=Flask-Testing-dev>`_

"""
import sys
from setuptools import setup

tests_require = [
    'twill',
    'blinker',
]

if sys.version_info < (2,6):
    tests_require.append('simplejson')

setup(
    name='Flask-Testing',
    version='0.4.1',
    url='https://github.com/jarus/flask-testing',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    description='Unit testing for Flask',
    long_description=__doc__,
    packages=['flask_testing'],
    test_suite="tests.suite",
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'multiprocessing',
    ],
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
