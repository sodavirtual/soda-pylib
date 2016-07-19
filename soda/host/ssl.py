from __future__ import absolute_import

from fabric.api import execute, run
from fabric.context_managers import cd, settings

from ..fabric.base import BaseTask
from soda.misc import display, get_effective_role, input


__all__ = [
    'create_cert',
    'renew_certs',
]


class CreateCert(BaseTask):
    """Create a standalone SSL certificate for the domains chain
    """

    name = 'create_cert'

    def run(self):
        from soda.host import nginx  # Import here to avoid wrong Fabric --list

        # Stop nginx first
        execute(nginx.stop)

        # Retrieve necessary information from the user
        email = input('Insert the certificate manager email address: ')
        domains = input('Insert the domains to apply: ').split()

        user = settings(user='root')
        cwd = cd(self.roledef.get('letsencrypt_dir', '/opt/letsencrypt'))
        warn_only = settings(warn_only=True)

        # Generate the certificate
        with user, cwd, warn_only:
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


class RenewCerts(BaseTask):
    """Renew SSL certificates
    """

    name = 'renew_certs'

    def run(self):
        from soda.host import nginx  # Import here to avoid wrong Fabric --list

        # Stop nginx first
        execute(nginx.stop)

        user = settings(user='root')
        cwd = cd(self.roledef.get('letsencrypt_dir', '/opt/letsencrypt'))
        warn_only = settings(warn_only=True)

        # Generate the certificate
        with user, cwd, warn_only:
            result = run('./letsencrypt-auto renew --standalone')

        # Display a result message
        if result.succeeded:
            display.success('SSL certificates were successfully renewed!')
        else:
            display.error(
                'Failed to renew SSL certificates.', abort_task=False)

        # Put nginx back up
        execute(nginx.start)


create_cert = CreateCert()
renew_certs = RenewCerts()
