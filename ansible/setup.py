#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='setup_github_watch',
    version="0.9.0",
    description="Ansible script for github_watch service",
    author_email='rem.baba@gmail.com',
    url='http://www.github.com/rembaba',
    install_requires=[
        'ansible',
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
        'run_ansible': [
            'ansible/*.yml',
        ]
    },
)
