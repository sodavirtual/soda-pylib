from __future__ import absolute_import

from fabric.api import run

from ..fabric.base import BaseTask
from soda.misc import display, lock_task


__all__ = [
    'collect_static',
    'migrate',
]


class CollectStaticTask(BaseTask):
    """Run Django's `collectstatic` management command
    """

    name = 'collect_static'

    @lock_task
    def run(self):
        display.info('Collecting static files...')
        with self.user, self.in_app, self.venv, self.django_settings:
            ignore = ' '.join(
                "--ignore '{}'".format(pattern) for pattern in [
                    'cdn', 'debug_toolbar', 'django_extensions', 'less',
                    'package.json', 'README*', 'scss',
                ])
            run('./manage.py collectstatic --noinput {}'.format(ignore))


class MigrateTask(BaseTask):
    """Run Django's `migrate` management command
    """

    name = 'migrate'

    @lock_task
    def run(self):
        display.info('Running database migrations...')
        with self.user, self.in_app, self.venv, self.django_settings:
            run('./manage.py migrate --noinput')


collect_static = CollectStaticTask()
migrate = MigrateTask()
