# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import jinja2

from simple_model.v2 import Model, Attribute, Unset
from simple_model.helpers import list_type

import pycli


TEMPLATE_DIR = os.path.join(os.path.dirname(pycli.__file__), 'assets')
ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


def valid_dir(path):
    if os.path.exists(path) and os.path.isfile(path):
        raise ValueError('File exists: {}'.format(path))

    return os.path.abspath(path)


def valid_file(path):
    if os.path.exists(path):
        raise ValueError('File exists: {}'.format(path))

    return os.path.abspath(path)


@Model()
@Attribute('path', type=valid_dir)
class Directory(object):
    def create(self):
        pycli.files.makedir(self.path, True)


@Model()
@Attribute('name', type=str)
class Template(object):
    def render(self, context=None):
        return ENVIRONMENT.get_template(self.name).render(context)


@Model()
@Attribute('path', type=valid_file)
@Attribute('context', type=dict, default={})
@Attribute('template', type=str, optional=True)
@Attribute('content', type=str, optional=True)
class File(object):
    def create(self):
        if self.template is not Unset:
            content = ENVIRONMENT.get_template(self.template).render(self.context)
        elif self.content is not Unset:
            content = self.content
        else:
            content = ''

        pycli.files.write(content, self.path)


@Model()
@Attribute('name', type=str)
@Attribute('email', type=str)
class Author(object):
    pass


@Model()
@Attribute('author', type=Author)
@Attribute('platforms', type=list_type(str), default=['linux'])
class Config(object):
    pass


@Model(hide_unset=True)
@Attribute('keywords', type=list_type(str), optional=True)
@Attribute('description', type=str, optional=True)
@Attribute('url', type=str, optional=True)
@Attribute('download_url', type=str, optional=True)
class ProjectConfig(Config):
    pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
