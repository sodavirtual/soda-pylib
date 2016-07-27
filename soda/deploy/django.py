from __future__ import absolute_import

from fabric.api import run

from ..fabric.base import ConflictingTask
from soda.misc import display


__all__ = [
    'collectstatic',
    'migrate',
]


class CollectStaticTask(ConflictingTask):
    """Run Django's `collectstatic` management command
    """

    name = 'collectstatic'

    def run(self):
        display.info('Collecting static files...')
        with self.user, self.in_app, self.venv, self.django_settings:
            ignore = ' '.join(
                "--ignore '{}'".format(pattern) for pattern in [
                    'cdn', 'debug_toolbar', 'django_extensions', 'less',
                    'package.json', 'README*', 'scss',
                ])
            run('./manage.py collectstatic --noinput {}'.format(ignore))


class MigrateTask(ConflictingTask):
    """Run Django's `migrate` management command
    """

    name = 'migrate'

    def run(self):
        display.info('Running database migrations...')
        with self.user, self.in_app, self.venv, self.django_settings:
            run('./manage.py migrate --noinput')


collectstatic = CollectStaticTask()
migrate = MigrateTask()
