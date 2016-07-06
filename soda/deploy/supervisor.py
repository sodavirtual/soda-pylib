from __future__ import absolute_import

from fabric.api import run, task
from fabric.context_managers import settings

from soda.misc import display, get_effective_role, lock_task


@task
@lock_task
def stop():
    """Stop the Supervisor service
    """
    role, roledef = get_effective_role()
    logged_user = settings(user=roledef['user'])
    with logged_user:
        display.info('Stopping the app...')
        run('supervisorctl stop {}'.format(roledef['service_name']))


@task
@lock_task
def start():
    """Start the Supervisor service
    """
    role, roledef = get_effective_role()
    logged_user = settings(user=roledef['user'])
    with logged_user:
        display.info('Starting the app...')
        run('supervisorctl start {}'.format(roledef['service_name']))
