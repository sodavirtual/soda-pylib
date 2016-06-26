from fabric.api import abort, env
from fabric.colors import blue, red


def get_effective_role():
    """Acquire the role definition according to current host
    """
    for role in env.roles:
        if env.host in env.roledefs[role]['hosts']:
            return role, env.roledefs[role]
    raise ValueError('Role undefined by {}'.format(env.host))


def info(msg):
    """Shortcut to display an info message
    """
    print(blue('\n{}'.format(msg)))


def error(msg):
    """Shortcut to abort a task and display an error message
    """
    abort(red(msg))
