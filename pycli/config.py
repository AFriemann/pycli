# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import json

from simple_tools import interaction, files as sm_os

from pycli import files, model


def find(root, maxdepth=None):
    for root, parent, _files in sm_os.walk_up(root, maxdepth):
        if '.pyclirc' in _files:
            return os.path.join(root, '.pyclirc')


def load(path, **kwargs):
    if not os.path.exists(path):
        config = write(create(path))
    else:
        try:
            with open(path, 'rb') as stream:
                config = json.loads(stream.read().decode())
        except json.decoder.JSONDecodeError:
            if interaction.confirm("Configuration invalid, recreate?"):
                config = write(create(path))
            else:
                raise RuntimeError("Invalid configuration")

    config.update(**kwargs)

    return config


def create(name=None, email=None):
    return model.Config(
        author=model.Author(
            name=interaction.collect('Author Name', name),
            email=interaction.collect('Author eMail', email),
        )
    )


def write(path, config):
    files.makedir(os.path.dirname(path), True)

    with open(path, 'wb') as stream:
        stream.write(json.dumps(dict(config)).encode())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
