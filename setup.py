# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

root = os.path.abspath(os.path.dirname(__file__))

version = __import__('events_watcher').__version__

with open(os.path.join(root, 'README.rst')) as f:
    README = f.read()

setup(
    name='django-events-watcher',
    version=version,
    description='Events watcher is an event packaging library for Django to track changes made in your models.',
    long_description=README,
    author='Florent Messa',
    author_email='florent.messa@gmail.com',
    url='http://github.com/thoas/django-events-watcher',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
