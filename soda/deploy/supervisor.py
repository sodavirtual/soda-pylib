from __future__ import absolute_import

from fabric.api import run
from fabric.context_managers import settings
from fabric.tasks import Task

from soda.misc import display, get_effective_role, lock_task


__all__ = [
    'stop',
    'start',
]


class StopTask(Task):
    """Stop the Supervisor service
    """

    name = 'stop'

    @lock_task
    def run(self):
        role, roledef = get_effective_role()
        logged_user = settings(user=roledef['user'])
        with logged_user:
            display.info('Stopping the app...')
            run('supervisorctl stop {}'.format(roledef['service_name']))


class StartTask(Task):
    """Start the Supervisor service
    """

    name = 'start'

    @lock_task
    def run(self):
        role, roledef = get_effective_role()
        logged_user = settings(user=roledef['user'])
        with logged_user:
            display.info('Starting the app...')
            run('supervisorctl start {}'.format(roledef['service_name']))


stop = StopTask()
start = StartTask()
