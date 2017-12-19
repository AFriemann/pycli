# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import logging
import inflection

from pycli import files, templates, config


logger = logging.getLogger(__name__)


def generate_project(directory, **kwargs):
    project_dir = os.path.abspath(directory)
    name = os.path.basename(os.path.abspath(directory))

    logger.info('creating project %s in %s', name, project_dir)

    # context = templates.build_context(name, project_dir, **kwargs)

    files.makedir(project_dir, True)

    generate_pycli_config(name, project_dir, **kwargs)
    generate_project_configs(name, project_dir, **kwargs)
    generate_project_tests(name, project_dir, **kwargs)
    generate_module(name, project_dir, **kwargs)


def generate_pycli_config(name, directory, **kwargs):
    # context = templates.build_context(name, directory, **kwargs)

    config.create(
        os.path.join(directory, '.pyclirc'),
        **kwargs.get('author', {})
    )


def generate_project_configs(name, directory, **kwargs):
    context = templates.build_context(inflection.underscore(name), directory, **kwargs)

    logger.info('creating config files for project %s in %s', name, directory)

    generate_license(name, directory, **kwargs)
    generate_readme(name, directory, **kwargs)

    files.write(
        'dist\n__pycache__\n*.egg-info\n*.pyc',
        os.path.join(directory, '.gitignore')
    )
    files.write(
        templates.render('setup.py.j2', context),
        os.path.join(directory, 'setup.py')
    )
    files.write(
        templates.render('setup.cfg.j2', context),
        os.path.join(directory, 'setup.cfg')
    )
    files.write(
        '',
        os.path.join(directory, 'requirements.txt')
    )
    files.write(
        'include *.rst *.txt *.md',
        os.path.join(directory, 'MANIFEST.in')
    )


def generate_readme(name, directory, **kwargs):
    context = templates.build_context(inflection.humanize(name), directory, **kwargs)

    logger.info('creating readme file for project %s in %s', name, directory)

    files.write(
        templates.render('README.rst.j2', context),
        os.path.join(directory, 'README.rst')
    )


def generate_license(name, directory, **kwargs):
    # context = templates.build_context(name, directory, **kwargs)

    logger.info('creating license file for project %s in %s', name, directory)

    files.write(
        '',
        os.path.join(directory, 'LICENSE.txt')
    )


def generate_project_tests(name, directory, **kwargs):
    context = templates.build_context(inflection.underscore(name), directory, **kwargs)
    test_dir = os.path.join(directory, 'tests')

    logger.info('creating test files for project %s in %s', name, directory)

    files.write(
        templates.render('tox.ini.j2', context),
        os.path.join(directory, 'tox.ini')
    )
    files.write(
        templates.render('coverage.cfg.j2', context),
        os.path.join(directory, 'coverage.cfg')
    )

    files.makedir(test_dir, True)
    files.write(
        '',
        os.path.join(test_dir, '__init__.py')
    )


def generate_module(name, directory, **kwargs):
    # context = templates.build_context(name, directory, **kwargs)
    path = os.path.join(directory, inflection.underscore(name))

    logger.info('creating module %s in %s', name, path)

    if os.path.exists(path):
        raise RuntimeError('File exists: {}'.format(path))

    files.makedir(path, True)
    files.write("__version__ = '0.0.0'", os.path.join(path, '__init__.py'))


def generate_class(name, directory, **kwargs):
    context = templates.build_context(inflection.camelize(name), directory, **kwargs)

    logger.info('creating class %s in %s', name, directory)

    path = os.path.join(directory, '{}.py'.format(inflection.underscore(name)))

    if os.path.exists(path):
        raise RuntimeError('File exists: {}'.format(path))

    files.write(
        templates.render('class.py.j2', context),
        path
    )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
