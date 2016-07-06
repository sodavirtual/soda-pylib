from __future__ import absolute_import

from fabric.api import abort
from fabric.colors import blue, green, red


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
