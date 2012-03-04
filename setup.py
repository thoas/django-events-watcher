# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = __import__('simple_events').__version__

setup(
    name='django-simple-events',
    version=version,
    description='Simple events is an event packaging library for Django.',
    author='Florent Messa',
    author_email='florent.messa@gmail.com',
    url='http://github.com/thoas/django-simple-events',
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
