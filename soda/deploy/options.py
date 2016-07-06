from __future__ import absolute_import

from fabric.api import abort, env, task
from fabric.colors import red

from soda.misc import input


@task
def force():
    """Mark the `force` flag
    """
    msg = 'You are forcing things. Are you aware of possible damages?'
    if input(red('{} (y/n) '.format(msg))) != 'y':
        abort('Wise.')
    env.force = True
