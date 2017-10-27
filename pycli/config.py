# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import os
import json

from simple_tools import interaction
from simple_model import Model, Attribute, list_type

from pycli import files


class Author(Model):
    name = Attribute(str)
    email = Attribute(str)

class Config(Model):
    author = Attribute(Author)
    platforms = Attribute(list_type(str), fallback=['linux'])

def load(path, **kwargs):
    if not os.path.exists(path):
        config = create(path)
    else:
        try:
            with open(path, 'rb') as stream:
                config = json.loads(stream.read().decode())
        except json.decoder.JSONDecodeError:
            if interaction.confirm("Configuration invalid, recreate?"):
                config = create(path)
            else:
                raise RuntimeError("Invalid configuration")

    config.update(**kwargs)

    return config

def create(path):
    files.makedir(os.path.dirname(path), True)

    config = Config(
        author = Author(
            name = input('Author name: '),
            email = input('Author email: '),
        )
    )

    with open(path, 'wb') as stream:
        stream.write(json.dumps(dict(config)).encode())

    return config

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
