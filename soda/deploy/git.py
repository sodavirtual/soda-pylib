from __future__ import absolute_import

from fabric.api import env, local, run, task
from fabric.context_managers import cd, hide, settings

from soda.misc import display, get_effective_role, lock_task


@task
def display_version():
    """Display current project revision
    """
    role, roledef = get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])

    display.info('Retrieving current app version...')
    with hide('everything'), logged_user, cwd:
        print(run('git log -1'))


@task
@lock_task
def update_sources(revision):
    """Fetch sources from default remote and checkout to revision
    """
    role, roledef = get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])

    with hide('everything'), logged_user, cwd:
        # Get the used remote name
        git_remote = run('git remote')

        # Update the app source code
        display.info('Fetching source code from "{}"...'.format(git_remote))
        print(run('git fetch -p {}'.format(git_remote)))

        # Check working directory
        display.info('Checking app directory...')
        git_status = run('git status --porcelain')
        if filter(lambda l: l and not l[:2] == '??', git_status.split('\n')):
            print(git_status)
            display.error('App directory is dirty.', abort_task=not env.force)

        # Check out to specified revision
        display.info('Checking out to specified revision...')
        print(run('git checkout -f {}/{}'.format(git_remote, revision)))


@task
def check_local_remote(revision):
    """Abort if local and remote ref don't match
    """
    role, roledef = get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])

    display.info('Checking local and remote revisions...')
    with hide('everything'), logged_user, cwd:
        # Check local revision
        local_branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
        if local_branch != revision:
            display.error(
                'You are currently not at {}.'.format(revision),
                abort_task=not env.force)

        # Get the hash of the latest commit in `revision` (remote)
        git_remote = run('git remote')
        remote_hash = run('git rev-parse --short --verify {}/{}'.format(
            git_remote, revision,
        ))

        # Get the hash of the latest commit in `revision` (local)
        local_hash = local(
            'git rev-parse --short --verify {}'.format(revision),
            capture=True
        )

    # Compare local and remote commit hashes
    if local_hash != remote_hash:
        display.error(
            'The local and remote revisions must match. You may need to '
            'update one of both of them.', abort_task=not env.force)

    display.success('Revisions match.')
