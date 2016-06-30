import os

from fabric.api import run, task
from fabric.context_managers import cd, prefix, settings, shell_env

from soda.deploy import misc


@task
def collectstatic():
    """Run Django's `collectstatic` management command
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])
    active_venv = prefix('source {}'.format(
        os.path.join(roledef['venv_path'], 'bin', 'activate')))
    django_settings = shell_env(
        DJANGO_SETTINGS_MODULE=roledef['settings_module'])

    misc.info('Collecting static files...')
    with logged_user, cwd, active_venv, django_settings:
        ignore = ' '.join(
            "--ignore '{}'".format(pattern) for pattern in [
                'cdn', 'debug_toolbar', 'django_extensions', 'less',
                'package.json', 'README*', 'scss',
            ])
        run('./manage.py collectstatic --noinput {}'.format(ignore))


@task
def migrate():
    """Run Django's `migrate` management command
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])
    active_venv = prefix('source {}'.format(
        os.path.join(roledef['venv_path'], 'bin', 'activate')))
    django_settings = shell_env(
        DJANGO_SETTINGS_MODULE=roledef['settings_module'])

    misc.info('Running database migrations...')
    with logged_user, cwd, active_venv, django_settings:
        run('./manage.py migrate --noinput')
