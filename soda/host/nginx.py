from fabric.api import abort, run, task
from fabric.colors import red
from fabric.context_managers import settings


@task
def stop():
    """Stop the nginx process
    """
    # Acquire the `input` function from Python 2 or 3
    try:
        input = raw_input
    except NameError:
        pass

    if input(red('Are you sure you want to stop nginx? (y/n) ')) != 'y':
        abort('Wise.')

    with settings(user='root'):
        run('nginx -s quit')


@task
def start():
    """Start the nginx process
    """
    with settings(user='root'):
        run('nginx')


@task
def reload():
    """reload the nginx process
    """
    with settings(user='root'):
        run('nginx -s reload')
