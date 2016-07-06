from __future__ import absolute_import

from fabric.api import env


# Acquire the `input` function from Python 2 or 3
try:
    input = raw_input
except NameError:
    input = input


def get_effective_role():
    """Acquire the role definition according to current host
    """
    for role in env.roles:
        if env.host in env.roledefs[role]['hosts']:
            return role, env.roledefs[role]
    raise ValueError('Role undefined by {}'.format(env.host))
