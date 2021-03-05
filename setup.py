#!/usr/bin/env python3
#
# ama-framework setup
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


from setuptools import setup, find_packages
from ama.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()


setup(
    name='ama',
    version=VERSION,
    description='ama allow you perform several attacks in a cluster',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='glozanoa',
    author_email='glozanoa@uni.pe',
    url='https://github.com/fpolit/ama-framework',
    license='GPL3',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'ama = ama.ama:main',
            'amadb = ama.amadb:main'
        ],
    }
)
