from __future__ import absolute_import
from functools import wraps
import os

from fabric.api import env, run
from fabric.context_managers import cd, hide, prefix, settings, shell_env
from fabric.contrib import files
from fabric.tasks import Task

from ..misc import display, get_effective_role


class BaseTask(Task):

    """An abstract class to provide core functionality to our Fabric tasks
    """

    def __getattribute__(self, name):
        """Support pre-run and post-run hooks
        """
        if name == 'run':
            orig_fn = super(BaseTask, self).__getattribute__('run')

            @wraps(orig_fn)
            def wrapper(*args, **kwargs):
                # Run the pre-run hook
                if hasattr(self, 'pre_run'):
                    self.pre_run()

                # Get the original task function
                orig_fn(*args, **kwargs)

                # Run the post-run hook
                if hasattr(self, 'post_run'):
                    self.post_run()

            return wrapper

        return super(BaseTask, self).__getattribute__(name)

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


class ConflictingTask(BaseTask):

    """Lock an environment for the execution of this task
    """

    def pre_run(self):
        """Check and create the lock file within the app dir
        """
        with self.user, self.in_app:
            file_exists = files.exists('soda-lock')

        if file_exists:
            msg = 'There is a conflicting operation ongoing or broken.'
            display.error(msg, abort_task=not env.force)

        with hide('everything'), self.user, self.in_app:
            run('touch soda-lock')

    def post_run(self):
        """Remove the lock file from the app dir
        """
        with hide('everything'), self.user, self.in_app:
            run('rm soda-lock')
