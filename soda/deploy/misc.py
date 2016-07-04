from fabric.api import abort, env
from fabric.colors import blue, green, red


# Acquire the `input` function from Python 2 or 3
try:
    input = raw_input
except NameError:
    pass


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


def error(msg, abort_task=True):
    """Shortcut to abort a task and display an error message
    """
    msg = red(msg)

    if abort_task:
        abort(msg)

    print(msg)


def success(msg):
    """Shorcut to display a success message
    """
    print(green('\n{}'.format(msg)))
