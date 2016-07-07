from __future__ import absolute_import

from fabric.api import run

from ..fabric.base import ConflictingTask
from soda.misc import display


__all__ = [
    'stop',
    'start',
]


class StopTask(ConflictingTask):
    """Stop the Supervisor service
    """

    name = 'stop'

    def run(self):
        with self.user:
            display.info('Stopping the app...')
            run('supervisorctl stop {}'.format(self.roledef['service_name']))


class StartTask(ConflictingTask):
    """Start the Supervisor service
    """

    name = 'start'

    def run(self):
        with self.user:
            display.info('Starting the app...')
            run('supervisorctl start {}'.format(self.roledef['service_name']))


stop = StopTask()
start = StartTask()
