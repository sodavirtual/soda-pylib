from fabric.api import abort, env, task
from fabric.colors import red

from soda.deploy import misc


@task
def force():
    """Mark the `force` flag
    """
    msg = 'You are forcing things. Are you aware of possible damages?'
    if misc.input(red('{} (y/n) '.format(msg))) != 'y':
        abort('Wise.')
    env.force = True
