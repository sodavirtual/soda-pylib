from __future__ import absolute_import

from fabric.api import abort, run
from fabric.colors import red
from fabric.context_managers import settings

from ..fabric.base import BaseTask
from soda.misc import display, input


__all__ = [
    'stop',
    'start',
    'reload',
]


class StopTask(BaseTask):
    """Stop the nginx process
    """

    name = 'stop'

    def run(self):
        if input(red('Are you sure you want to stop nginx? (y/n) ')) != 'y':
            abort('Wise.')

        display.info('Stopping nginx...')
        with settings(user='root'):
            run('nginx -s quit')


class StartTask(BaseTask):
    """Start the nginx process
    """

    name = 'start'

    def run(self):
        display.info('Starting nginx...')
        with settings(user='root'):
            run('nginx')


class ReloadTask(BaseTask):
    """reload the nginx process
    """

    name = 'reload'

    def run(self):
        display.info('Reloading nginx configuration...')
        with settings(user='root'):
            run('nginx -s reload')

stop = StopTask()
start = StartTask()
reload = ReloadTask()
