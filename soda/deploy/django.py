from __future__ import absolute_import
import os

from fabric.api import run
from fabric.context_managers import cd, prefix, settings, shell_env

from ..fabric.base import BaseTask
from soda.misc import display, get_effective_role, lock_task


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
        role, roledef = get_effective_role()
        logged_user = settings(user=roledef['user'])
        cwd = cd(roledef['app_path'])
        active_venv = prefix('source {}'.format(
            os.path.join(roledef['venv_path'], 'bin', 'activate')))
        django_settings = shell_env(
            DJANGO_SETTINGS_MODULE=roledef['settings_module'])

        display.info('Collecting static files...')
        with logged_user, cwd, active_venv, django_settings:
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
        role, roledef = get_effective_role()
        logged_user = settings(user=roledef['user'])
        cwd = cd(roledef['app_path'])
        active_venv = prefix('source {}'.format(
            os.path.join(roledef['venv_path'], 'bin', 'activate')))
        django_settings = shell_env(
            DJANGO_SETTINGS_MODULE=roledef['settings_module'])

        display.info('Running database migrations...')
        with logged_user, cwd, active_venv, django_settings:
            run('./manage.py migrate --noinput')


collect_static = CollectStaticTask()
migrate = MigrateTask()
