# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os

from pycli import files, templates


def pick(kind):
    if kind == 'project':
        return generate_project
    elif kind == 'module':
        return generate_module
    elif kind == 'class':
        return generate_class

    raise ValueError(kind)

def generate_project(name, directory, **kwargs):
    context = templates.build_context(name, directory, **kwargs)
    project_dir = os.path.join(directory, name)

    files.makedir(project_dir, True)
    files.write(
            templates.render('setup.py.j2', context),
            os.path.join(project_dir, 'setup.py')
    )
    files.write(
            'dist\n__pycache__\n*.egg-info\n*.pyc',
            os.path.join(project_dir, '.gitignore')
    )
    generate_module(name, project_dir)

def generate_module(name, directory, **kwargs):
    context = templates.build_context(name, directory, **kwargs)
    module_dir = os.path.join(directory, name)

    files.makedir(module_dir, True)
    files.write("__version__ = '0.0.0'", os.path.join(module_dir, '__init__.py'))

def generate_class(name, directory, **kwargs):
    context = templates.build_context(name, directory, **kwargs)

    files.write(
        templates.render('class.py.j2', context),
        os.path.join(directory, '{}.py'.format(name.lower()))
    )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
