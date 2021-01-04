#!/usr/bin/env python3
from setuptools import setup, find_packages
from mattack.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='mattack',
    version=VERSION,
    description='mattack allow you perform parallel Mask Attacks in a cluster.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='glozanoa',
    author_email='glozanoa@uni.pe',
    url='https://gitlab.com/spolit/mattack.git',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    #package_data={'mattack': ['templates/*']},
    install_requires=[
        "cement",
        "sbash",
        "fineprint",
    ],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        mattack = mattack.attack:main
    """,
)
