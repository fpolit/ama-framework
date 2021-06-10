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
    description='Specialized environment for the password cracking process',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='glozanoa',
    author_email='glozanoa@uni.pe',
    url='https://github.com/fpolit/ama-framework',
    license='GPL3',
    packages=find_packages(),
    package_data={
        "ama.core.plugins.auxiliary.wordlists": ["cupp.cfg"],
    },
    install_requires = [
        'fineprint',
        'sbash',
        'random-password-generator',
        'cmd2',
        'tabulate',
        'varname',
        'psutil',
        'name-that-hash',
        'search-that-hash',
        'hashid',
        'cupp'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'ama = ama.ama:main',
            'amadb = ama.amadb:main',
        ],
    }
)
