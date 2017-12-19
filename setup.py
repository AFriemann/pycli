# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os
import pip

try:
    from setuptools import setup, find_packages
except ImportError:
    print('Python2 detected, trying workaround')
    from distutils.core import setup, find_packages

from pycli import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()


INSTALL_REQS = pip.req.parse_requirements(
    'requirements.txt',
    session=pip.download.PipSession()
)

REQUIREMENTS = [str(ir.req) for ir in INSTALL_REQS if ir is not None]

if not __version__ or __version__ == '<VERSION>':
    raise RuntimeError("Package version not set!")

setup(name="pycli",
      author="Aljosha Friemann",
      author_email="a.friemann@automate.wtf",
      description="",
      keywords=[],
      version=__version__,
      license=read('LICENSE.txt'),
      long_description=read('README.rst'),
      install_requires=[],
      classifiers=[],
      packages=find_packages(exclude=('tests', 'assets')),
      entry_points={ 'console_scripts': ['pycli=pycli.cli:root'] },
      include_package_data=True,
      package_data={'': ['assets/*']},
      platforms='linux')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
