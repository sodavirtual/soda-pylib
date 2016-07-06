from __future__ import absolute_import

from fabric.api import abort, run, task
from fabric.colors import red
from fabric.context_managers import settings

from soda.misc import display, input


@task
def stop():
    """Stop the nginx process
    """
    if input(red('Are you sure you want to stop nginx? (y/n) ')) != 'y':
        abort('Wise.')

    display.info('Stopping nginx...')
    with settings(user='root'):
        run('nginx -s quit')


@task
def start():
    """Start the nginx process
    """
    display.info('Starting nginx...')
    with settings(user='root'):
        run('nginx')


@task
def reload():
    """reload the nginx process
    """
    display.info('Reloading nginx configuration...')
    with settings(user='root'):
        run('nginx -s reload')
