# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import click

from pycli import generators, config

@click.group()
@click.option('--configfile', '-c', type=click.Path(dir_okay=False), default=os.path.expanduser('~/.config/pycli/config.json'))
@click.pass_context
def root(ctx, configfile):
    ctx.obj = config.load(configfile)

@root.command()
@click.option('--keyword', '-k', multiple=True)
@click.option('--platform', '-p', multiple=True)
@click.argument('kind', type=click.Choice(['project', 'module', 'class']))
@click.argument('name')
@click.argument('directory', default=os.getcwd(), type=click.Path())
@click.pass_context
def generate(ctx, keyword, platform, kind, name, directory):
    generators.pick(kind)(
        name,
        directory,
        keywords=keyword,
        platforms=platform,
        **dict(ctx.obj)
    )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
