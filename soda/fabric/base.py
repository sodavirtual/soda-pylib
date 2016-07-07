from __future__ import absolute_import
import os

from fabric.context_managers import cd, prefix, settings, shell_env
from fabric.tasks import Task

from ..misc import get_effective_role


class BaseTask(Task):

    """An abstract class to provide core functionality to our Fabric tasks
    """

    @property
    def roledef(self):
        """A shortcut to the active roledef
        """
        role, roledef = get_effective_role()
        roledef['name'] = role  # Make the def aware of the role name
        return roledef

    @property
    def in_app(self):
        """Wrap a Fabric's context manager to switch to the role's app_path
        """
        return cd(self.roledef['app_path'])

    @property
    def user(self):
        """Wrap a Fabric's context manager to log in as the role's user
        """
        return settings(user=self.roledef['user'])

    @property
    def venv(self):
        """Wrap a Fabric's context manager to activate a virtual env
        """
        return prefix('source {}'.format(
            os.path.join(self.roledef['venv_path'], 'bin', 'activate')),
        )

    @property
    def django_settings(self):
        """Wrap a Fabric's context manager to set the Django settings module
        """
        return shell_env(
            DJANGO_SETTINGS_MODULE=self.roledef['settings_module'],
        )
