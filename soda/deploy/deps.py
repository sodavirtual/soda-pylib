import os

from fabric.api import run, task
from fabric.context_managers import cd, prefix, settings

from soda.deploy import misc, lock


@task
@lock.lock_task
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
@lock.lock_task
def install_bower_libs():
    """Install or update front-end dependencies from Bower
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])

    misc.info('Updating front-end dependencies...')
    with logged_user, cwd:
        run('bower install')
