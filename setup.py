#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    entry_points={
        'console_scripts': [
            'github_watch=github_watch.monitor:main',
        ],
    },
    name='github_watch',
    version="0.9.0",
    description='Monitoring and notification services for github',
    author_email='rem.baba@gmail.com',
    url='http://www.github.com/rembaba',
    install_requires=[
        'requests>=2.8.1',
        'PyYAML>=3.11',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=('tests' 'tests.*' 'build.*',)),
    package_data={
        'cmdline': [
            'github_watch/config/*.yml',
            'github_watch/ansible/*.yml',
        ]
    },
)
