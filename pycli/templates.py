# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import jinja2
import logging

import pycli


logger = logging.getLogger(__name__)

TEMPLATE_DIR=os.path.join(os.path.dirname(pycli.__file__), 'assets')

def render(name, context):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

    logger.debug('Trying to render template %s with context %s', name, context)

    return environment.get_template(name).render(context)

def build_context(name, directory, **kwargs):
    context = {}
    context.update(name=name, directory=directory, **kwargs)

    return context

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
