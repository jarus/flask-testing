"""
Flask-Testing
-------------

Flask unittest integration.

Links
`````

* `documentation <http://packages.python.org/Flask-Testing>`
* `development version <http://github.com/jarus/flask-testing/zipball/master#egg=Flask-Testing-dev>`

"""
import sys
from setuptools import setup

tests_require = [
    'blinker'
]

install_requires = [
    'Flask'
]

if sys.version_info[0] < 3:
    tests_require.append('twill==0.9.1')

if sys.version_info < (2, 6):
    tests_require.append('simplejson')
    install_requires.append('multiprocessing')

setup(
    name='Flask-Testing',
    version='0.8.2',
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
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
