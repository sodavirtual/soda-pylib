from __future__ import absolute_import

from fabric.api import local
from fabric.decorators import runs_once

from ..fabric.base import BaseTask
from soda.misc import display


__all__ = [
    'register_deploy',
]


BASE_URL = 'https://intake.opbeat.com/api/v1'


class RegisterDeployTask(BaseTask):
    """Register deployment to Opbeat
    """

    name = 'register_deploy'

    @runs_once
    def run(self):
        display.info('Registering deployment to Opbeat...')

        # Do not communicate to Opbeat if it's not set up
        if 'opbeat' not in self.roledef:
            display.warning(
                'Opbeat is not set up for {}'.format(self.roledef['name']))
            return

        revision = local('git log -n 1 --pretty="format:%H"', capture=True)
        branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
        local((
            'curl {base_url}/organizations/{opbeat[ORGANIZATION_ID]}/apps'
            '/{opbeat[APP_ID]}/releases/'
            ' -H "Authorization: Bearer {opbeat[SECRET_TOKEN]}"'
            ' -d rev={rev}'
            ' -d branch={branch}'
            ' -d status=completed').format(
                base_url=BASE_URL,
                opbeat=self.roledef['opbeat'],
                rev=revision,
                branch=branch,
        ))


register_deploy = RegisterDeployTask()
