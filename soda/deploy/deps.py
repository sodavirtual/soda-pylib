import os

from fabric.api import run, task, local
from fabric.context_managers import cd, prefix, settings

from soda.deploy import misc


@task
def install_python_libs():
    """Install or update Python dependencies from `requirements.txt`
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])
    active_venv = prefix('source {}'.format(
        os.path.join(roledef['venv_path'], 'bin', 'activate')))

    misc.info('Updating Python dependencies...')
    with logged_user, cwd, active_venv:
        run('pip install -r requirements.txt')


@task
def install_bower_libs():
    """Install or update front-end dependencies from Bower
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])

    misc.info('Updating front-end dependencies...')
    with logged_user, cwd:
        run('bower install')


@task
def verify_lock_file():
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    with logged_user:
        return run('[ -e deploy.lock ] && echo 1 || echo 0 ')


@task
def create_lock_file():
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    with logged_user:
        local('touch deploy.lock')


@task
def delete_lock_file():
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    with logged_user:
        local('rm deploy.lock')
