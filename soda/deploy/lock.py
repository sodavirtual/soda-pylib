from fabric.api import run, task, local
from fabric.context_managers import settings

from soda.deploy import misc


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
