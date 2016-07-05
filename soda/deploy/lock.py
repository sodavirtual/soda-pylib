import os.path

from fabric.api import cd, env, hide, run
from fabric.context_managers import settings
from fabric.contrib import files

from soda.deploy import misc


class lock_task(object):

    """A decorator that creates a `lock` file for a Fabric task
    """

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        role, roledef = misc.get_effective_role()

        with settings(user=roledef['user']):
            lock_file = os.path.join(roledef['app_path'], 'soda-lock')
            file_exists = files.exists(lock_file)

        if file_exists:
            msg = 'There is a conflicting operation ongoing or broken.'
            misc.error(msg, abort_task=not env.force)

        logged_user = settings(user=roledef['user'])
        cwd = cd(roledef['app_path'])
        with hide('everything'), logged_user, cwd:
            run('touch soda-lock')

        self.fn(*args, **kwargs)

        logged_user = settings(user=roledef['user'])
        cwd = cd(roledef['app_path'])
        with hide('everything'), logged_user, cwd:
            run('rm soda-lock')
