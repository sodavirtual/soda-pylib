from fabric.api import run, task
from fabric.context_managers import cd, hide, settings

from soda.deploy import misc


@task
def display_version():
    """Display current project revision
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])

    misc.info('Retrieving current app version...')
    with hide('everything'), logged_user, cwd:
        print(run('git log -1'))


@task
def update_sources(revision):
    """Fetch sources from default remote and checkout to revision
    """
    role, roledef = misc.get_effective_role()
    logged_user = settings(user=roledef['user'])
    cwd = cd(roledef['app_path'])

    with hide('everything'), logged_user, cwd:
        # Get the used remote name
        git_remote = run('git remote')

        # Update the app source code
        misc.info('Fetching source code from "{}"...'.format(git_remote))
        print(run('git fetch -p {}'.format(git_remote)))

        # Check working directory
        misc.info('Checking app directory...')
        git_status = run('git status --porcelain')
        if filter(lambda l: l and not l[:2] == '??', git_status.split('\n')):
            print(git_status)
            misc.error('App directory is dirty.')

        # Check out to specified revision
        misc.info('Checking out to specified revision...')
        print(run('git checkout -f {}/{}'.format(git_remote, revision)))
