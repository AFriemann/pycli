# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os


def makedir(path, exist_ok=False):
    try:
        os.makedirs(path, exist_ok=exist_ok)
    except TypeError:
        os.makedirs(path)


def write(data, path):
    with open(path, 'wb') as stream:
        stream.write(data.encode())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
