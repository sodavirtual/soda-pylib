from fabric.api import abort, run, task
from fabric.colors import red
from fabric.context_managers import settings

from soda.deploy import misc


@task
def stop():
    """Stop the nginx process
    """
    if misc.input(red('Are you sure you want to stop nginx? (y/n) ')) != 'y':
        abort('Wise.')

    misc.info('Stopping nginx...')
    with settings(user='root'):
        run('nginx -s quit')


@task
def start():
    """Start the nginx process
    """
    misc.info('Starting nginx...')
    with settings(user='root'):
        run('nginx')


@task
def reload():
    """reload the nginx process
    """
    misc.info('Reloading nginx configuration...')
    with settings(user='root'):
        run('nginx -s reload')
