#!/usr/bin/env python3
from setuptools import setup, find_packages
from hattack.utilities.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='hattack',
    version=VERSION,
    description='hattack allow you perform several hash attacks in a cluster',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='glozanoa',
    author_email='glozanoa@uni.pe',
    url='https://gitlab.com/spolit/hattack.git',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    #package_data={'mattack': ['templates/*']},
    install_requires=[
        "cement",
        "sbash",
        "fineprint",
    ],
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'hattack = hattack.cli.attack:main',
            'hsearch = hattack.cli.search:main',
            'hstatus = hattack.cli.status:main',
            'hcombine = hattack.cli.combinator:main'
        ]
    },
)
