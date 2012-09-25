# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = __import__('events_watcher').__version__

setup(
    name='django-events-watcher',
    version=version,
    description='Events watcher is an event packaging library for Django to track changes made in your models.',
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
