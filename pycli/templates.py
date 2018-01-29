# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""


def build_context(name, directory, **kwargs):
    context = {}
    context.update(name=name, directory=directory, **kwargs)

    return context

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
