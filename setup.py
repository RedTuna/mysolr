# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


REQUIRED = ['requests']
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
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
      version='0.6',
      description='Solr Python binding',
      long_description = open('README.rst').read(),
      author='Rubén Abad, Miguel Olivares',
      author_email='ruabag@gmail.com, miguel@moliware.com',
      url='http://mysolr.redtuna.org',
      packages=['mysolr'],
      install_requires=REQUIRED,
      tests_require=['unittest2'],
      test_suite='unittest2.collector',
      classifiers=CLASSIFIERS)
