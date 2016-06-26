from fabric.api import run, task
from fabric.context_managers import settings

from soda.deploy import misc


@task
def stop():
    """Stop the Supervisor service
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    with logged_user:
        misc.info('Stopping the app...')
        run('supervisorctl stop {}'.format(roledef['service_name']))


@task
def start():
    """Start the Supervisor service
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    with logged_user:
        misc.info('Starting the app...')
        run('supervisorctl start {}'.format(roledef['service_name']))
