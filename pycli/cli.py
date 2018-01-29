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


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


def check_requirements():
    if not shutil.which('git'):
        raise RuntimeError('PyCli needs git installed!')


@click.command(cls=AliasedGroup)
@click.option('--configfile', '-c',
              type=click.Path(dir_okay=False),
              default=os.path.expanduser('~/.config/pycli/config.json'))
@click.pass_context
def root(ctx, configfile):
    logging.basicConfig(level=logging.INFO)

    check_requirements()

    ctx.obj = config.load(configfile)

    next_config = config.find(os.getcwd())

    if next_config is not None:
        ctx.obj.update(**config.load(next_config))


@root.command()
@click.option('--keyword', '-k', multiple=True)
@click.option('--platform', '-p', multiple=True)
@click.option('--description', '-d')
@click.option('--url', '-u')
@click.option('--download-url')
@click.argument('directory', default=os.getcwd(), type=click.Path())
@click.pass_context
def new(ctx, keyword, platform, description, url, download_url, directory):
    project_files = generators.generate_project(
        directory,
        keywords=keyword,
        platforms=platform,
        **dict(ctx.obj)
    )

    for obj in project_files:
        obj.create()


@root.command(cls=AliasedGroup)
@click.pass_context
def generate(ctx):
    pass

    # project_config = config.find(os.getcwd())
    #
    # if project_config is not None:
    #     ctx.obj.update(**config.load(project_config))


@generate.command(name='module')
@click.argument('name')
@click.argument('directory', default=os.getcwd(), type=click.Path())
@click.pass_context
def gen_module(ctx, name, directory):
    for obj in generators.generate_module(name, directory, **dict(ctx.obj)):
        obj.create()


@generate.command(name='class')
@click.argument('name')
@click.argument('directory', default=os.getcwd(), type=click.Path())
@click.pass_context
def gen_class(ctx, name, directory):
    for obj in generators.generate_class(name, directory, **dict(ctx.obj)):
        obj.create()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
