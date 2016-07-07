from __future__ import absolute_import

from fabric.api import run

from ..fabric.base import BaseTask
from soda.misc import display, lock_task


__all__ = [
    'stop',
    'start',
]


class StopTask(BaseTask):
    """Stop the Supervisor service
    """

    name = 'stop'

    @lock_task
    def run(self):
        with self.user:
            display.info('Stopping the app...')
            run('supervisorctl stop {}'.format(self.roledef['service_name']))


class StartTask(BaseTask):
    """Start the Supervisor service
    """

    name = 'start'

    @lock_task
    def run(self):
        with self.user:
            display.info('Starting the app...')
            run('supervisorctl start {}'.format(self.roledef['service_name']))


stop = StopTask()
start = StartTask()
