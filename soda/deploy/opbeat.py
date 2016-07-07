from __future__ import absolute_import

from fabric.api import local
from fabric.decorators import runs_once
from fabric.tasks import Task

from soda.misc import display, get_effective_role


__all__ = [
    'register_deploy',
]


BASE_URL = 'https://intake.opbeat.com/api/v1'


class RegisterDeployTask(Task):
    """Register deployment to Opbeat
    """

    name = 'register_deploy'

    @runs_once
    def run(self):
        role, roledef = get_effective_role()

        display.info('Registering deployment to Opbeat...')
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
                opbeat=roledef['opbeat'],
                rev=revision,
                branch=branch,
        ))

register_deploy = RegisterDeployTask()
