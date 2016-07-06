from __future__ import absolute_import

from fabric.api import env

from . import *
from ..host import *


__all__ = [
    'deps',
    'django',
    'git',
    'nginx',
    'options',
    'opbeat',
    'ssl',
    'supervisor',
]


# Register some global options
env.force = False
