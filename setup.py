# -*- coding: utf-8 -*-
from distutils.core import setup


REQUIRED = ['requests==0.10.1']
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]


setup(name='mysolr',
      version='0.5',
      description='Solr Python binding',
      long_description = open('README.rst').read(),
      author='Rubén Abad, Miguel Olivares',
      author_email='ruabag@gmail.com, miguel@moliware.com',
      url='http://mysolr.redtuna.org',
      packages=['mysolr'],
      install_requires=REQUIRED,
      classifiers=CLASSIFIERS)
