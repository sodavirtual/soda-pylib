from __future__ import absolute_import

from fabric.api import run

from ..fabric.base import ConflictingTask
from soda.misc import display


__all__ = [
    'install_python_libs',
    'install_bower_libs',
]


class InstallPythonLibsTask(ConflictingTask):
    """Install or update Python dependencies from `requirements.txt`
    """

    name = 'install_python_libs'

    def run(self):
        display.info('Updating Python dependencies...')
        with self.user, self.in_app, self.venv:
            run('pip install -r requirements.txt')


class InstallBowerLibsTask(ConflictingTask):
    """Install or update front-end dependencies from Bower
    """

    name = 'install_bower_libs'

    def run(self):
        display.info('Updating front-end dependencies...')
        with self.user, self.in_app:
            run('bower install')

install_python_libs = InstallPythonLibsTask()
install_bower_libs = InstallBowerLibsTask()
