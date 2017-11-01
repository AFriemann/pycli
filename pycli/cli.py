# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import click
import logging
import shutil

from pycli import generators, config

def check_requirements():
    if not shutil.which('git'):
        raise RuntimeError('PyCli needs git installed!')

@click.group()
@click.option('--configfile', '-c', type=click.Path(dir_okay=False), default=os.path.expanduser('~/.config/pycli/config.json'))
@click.pass_context
def root(ctx, configfile):
    logging.basicConfig(level=logging.INFO)

    check_requirements()

    ctx.obj = config.load(configfile)

@root.group()
def generate():
    pass

@generate.command(name='project')
@click.option('--keyword', '-k', multiple=True)
@click.option('--platform', '-p', multiple=True)
@click.argument('directory', default=os.getcwd(), type=click.Path())
@click.pass_context
def gen_project(ctx, keyword, platform, directory):
    generators.generate_project(
        directory,
        keywords=keyword, platforms=platform, **dict(ctx.obj)
    )

@generate.command(name='module')
@click.argument('name')
@click.argument('directory', default=os.getcwd(), type=click.Path())
@click.pass_context
def gen_module(ctx, name, directory):
    generators.generate_module(
        name, directory,
        **dict(ctx.obj)
    )

@generate.command(name='class')
@click.argument('name')
@click.argument('directory', default=os.getcwd(), type=click.Path())
@click.pass_context
def gen_class(ctx, name, directory):
    generators.generate_class(
        name, directory,
        **dict(ctx.obj)
    )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
