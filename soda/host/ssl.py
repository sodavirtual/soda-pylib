from __future__ import absolute_import

from fabric.api import execute, run, task
from fabric.context_managers import cd, settings

from soda.misc import display, get_effective_role, input


@task
def create_cert():
    """Create a standalone SSL certificate for the domains chain
    """
    from soda.host import nginx  # Import here to avoid wrong Fabric --list

    # Stop nginx first
    execute(nginx.stop)

    # Retrieve necessary information from the user
    email = input('Insert the certificate manager email address: ')
    domains = input('Insert the domains to apply: ').split()

    role, roledef = get_effective_role()
    logged_user = settings(user='root')
    cwd = cd(roledef.get('letsencrypt_dir', '/opt/letsencrypt'))
    warn_only = settings(warn_only=True)

    # Generate the certificate
    with logged_user, cwd, warn_only:
        result = run((
            './letsencrypt-auto certonly --standalone '
            '--email {email} {domains}'
            .format(
                email=email,
                domains=' '.join('-d {}'.format(d) for d in domains),
            )
        ))

    # Display a result message
    if result.succeeded:
        display.success('Key chain successfully created!')
    else:
        display.error('Failed to create key chain.', abort_task=False)

    # Put nginx back up
    execute(nginx.start)


@task
def renew_certs():
    """Renew SSL certificates
    """
    from soda.host import nginx  # Import here to avoid wrong Fabric --list

    # Stop nginx first
    execute(nginx.stop)

    role, roledef = get_effective_role()
    logged_user = settings(user='root')
    cwd = cd(roledef.get('letsencrypt_dir', '/opt/letsencrypt'))
    warn_only = settings(warn_only=True)

    # Generate the certificate
    with logged_user, cwd, warn_only:
        result = run('./letsencrypt-auto renew --standalone')

    # Display a result message
    if result.succeeded:
        display.success('SSL certificates were successfully renewed!')
    else:
        display.error('Failed to renew SSL certificates.', abort_task=False)

    # Put nginx back up
    execute(nginx.start)
