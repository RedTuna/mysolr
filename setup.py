# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


TEST_REQUIRED = None
if sys.version_info >= (3, ):
    TEST_REQUIRED = ['unittest2py3k']
elif sys.version_info >= (2, ):
    TEST_REQUIRED = ['unittest2']


REQUIRED = ['requests']
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]


setup(name='mysolr',
      version='0.6.1',
      description='Solr Python binding',
      long_description = open('README.rst').read(),
      author='Rubén Abad, Miguel Olivares',
      author_email='ruabag@gmail.com, miguel@moliware.com',
      url='http://mysolr.redtuna.org',
      packages=['mysolr'],
      install_requires=REQUIRED,
      tests_require=TEST_REQUIRED,
      test_suite='unittest2.collector',
      classifiers=CLASSIFIERS)
