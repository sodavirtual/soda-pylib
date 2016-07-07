from __future__ import absolute_import
import os

from fabric.api import run
from fabric.context_managers import cd, prefix, settings

from ..fabric.base import BaseTask
from soda.misc import display, get_effective_role, lock_task


__all__ = [
    'install_python_libs',
    'install_bower_libs',
]


class InstallPythonLibsTask(BaseTask):
    """Install or update Python dependencies from `requirements.txt`
    """

    name = 'install_python_libs'

    @lock_task
    def run(self):
        role, roledef = get_effective_role()
        logged_user = settings(user=roledef['user'])
        cwd = cd(roledef['app_path'])
        active_venv = prefix('source {}'.format(
            os.path.join(roledef['venv_path'], 'bin', 'activate')))

        display.info('Updating Python dependencies...')
        with logged_user, cwd, active_venv:
            run('pip install -r requirements.txt')


class InstallBowerLibsTask(BaseTask):
    """Install or update front-end dependencies from Bower
    """

    name = 'install_bower_libs'

    @lock_task
    def run(self):
        role, roledef = get_effective_role()
        logged_user = settings(user=roledef['user'])
        cwd = cd(roledef['app_path'])

        display.info('Updating front-end dependencies...')
        with logged_user, cwd:
            run('bower install')

install_python_libs = InstallPythonLibsTask()
install_bower_libs = InstallBowerLibsTask()
