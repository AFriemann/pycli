# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import json
import logging
import inflection

from simple_tools import interaction

from pycli import model


logger = logging.getLogger(__name__)


def build_context(name, directory, **kwargs):
    context = {}
    context.update(name=name, directory=directory, **kwargs)

    return context


def generate_project(directory, **kwargs):
    project_dir = os.path.abspath(directory)
    name = os.path.basename(project_dir)

    kwargs['author'].update(
        name=interaction.collect('Author Name', kwargs['author'].get('name')),
        email=interaction.collect('Author eMail', kwargs['author'].get('email')),
    )

    yield model.Directory(path=project_dir)

    yield from generate_pycli_config(name, project_dir, **kwargs)
    yield from generate_project_configs(name, project_dir, **kwargs)
    yield from generate_project_tests(name, project_dir, **kwargs)
    yield from generate_project_makefile(name, project_dir, **kwargs)
    yield from generate_module(name, project_dir, version='0.0.0', **kwargs)


def generate_pycli_config(name, directory, **kwargs):
    config = model.ProjectConfig(**kwargs)

    yield model.File(
        path=os.path.join(directory, '.pyclirc'),
        content=json.dumps(dict(config)),
    )


def generate_project_makefile(name, directory, **kwargs):
    context = build_context(
        inflection.titleize(name),
        directory,
        module_name=inflection.underscore(name),
        **kwargs
    )

    yield model.File(
        path=os.path.join(directory, 'Makefile'),
        template='Makefile.j2',
        context=context,
    )


def generate_project_configs(name, directory, **kwargs):
    context = build_context(inflection.underscore(name), directory, **kwargs)

    yield from generate_license(name, directory, **kwargs)
    yield from generate_readme(name, directory, **kwargs)

    yield model.File(
        path=os.path.join(directory, '.gitignore'),
        content='dist\n__pycache__\n*.egg-info\n*.pyc\n.tox\n.pyclirc',
    )

    yield model.File(
        path=os.path.join(directory, 'setup.py'),
        template='setup.py.j2',
        context=context
    )

    yield model.File(
        path=os.path.join(directory, 'setup.cfg'),
        template='setup.cfg.j2',
        context=context
    )

    yield model.File(
        path=os.path.join(directory, 'requirements.txt'),
        content='.'
    )

    yield model.File(
        path=os.path.join(directory, 'MANIFEST.in'),
        content='include *.rst *.txt *.md',
    )


def generate_readme(name, directory, **kwargs):
    context = build_context(
        inflection.titleize(name),
        directory,
        module_name=inflection.underscore(name),
        **kwargs
    )

    yield model.File(
        path=os.path.join(directory, 'README.rst'),
        template='README.rst.j2',
        context=context,
    )


def generate_license(name, directory, **kwargs):
    yield model.File(
        path=os.path.join(directory, 'LICENSE.txt')
    )


def generate_project_tests(name, directory, **kwargs):
    context = build_context(inflection.underscore(name), directory, **kwargs)

    test_dir = os.path.join(directory, 'tests')

    yield model.File(
        path=os.path.join(directory, 'tox.ini'),
        template='tox.ini.j2',
        context=context,
    )
    yield model.File(
        path=os.path.join(directory, 'coverage.cfg'),
        template='coverage.cfg.j2',
        context=context,
    )

    yield model.Directory(path=test_dir)

    yield model.File(
        path=os.path.join(test_dir, '__init__.py'),
    )


def generate_module(name, directory, version=None, **kwargs):
    path = os.path.join(directory, inflection.underscore(name))

    yield model.Directory(path=path)

    yield model.File(
        path=os.path.join(path, '__init__.py'),
        content="__version__ = '%s'" % version if version is not None else '',
    )


def generate_class(name, directory, **kwargs):
    path = os.path.join(directory, '{}.py'.format(inflection.underscore(name)))
    context = build_context(inflection.camelize(name), directory, **kwargs)

    yield model.File(
        path=path,
        template='class.py.j2',
        context=context,
    )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
