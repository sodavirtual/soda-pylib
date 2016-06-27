# soda-pylib

This is a bucket of Pythonic utilities to help developing and maintaining
projets at SODA Virtual.


## soda.deploy

A collection of Fabric tasks that will aid deploying projects to *Virtual
Private Servers*. They will require an `env.roledefs` to work properly:

```python
from fabric.api import env

env.roledefs = {
    'dev': {
        'app_path': '/path/to/project/repository',  # Full path!
        'hosts': ['my_app.sodateste.com.br'],  #  Can be more than one
        'service_name': 'my_app',  # Supervisor service name
        'settings_module': 'my_app.settings_dev',  # Django settings module
        'user': 'soda',  # System user to perform operations
        'venv_path': '/path/to/project/venv',  # Virtualenv path
    },
    'prod': {
        # ...
    },
}
```

The following tasks are available for use:

### `git.display_version`

Display the active revision at the remote host.

```python
from fabric.api import execute
from soda.deploy import git
execute(git.display_version)
```


### `git.update_sources`

Fetch sources from the default remote (acquired by `git remote`) and checkout
to specified revision.

```python
from fabric.api import execute
from soda.deploy import git
execute(git.update_sources, 'master')
```


### `supervisor.stop`

Stop the app's Supervisor main service.

```python
from fabric.api import execute
from soda.deploy import supervisor
execute(supervisor.stop)
```


### `supervisor.start`

Start the app's Supervisor main service.

```python
from fabric.api import execute
from soda.deploy import supervisor
execute(supervisor.start)
```


### `deps.install_python_libs`

Install Python dependencies as defined in the project's `requirements.txt`.

```python
from fabric.api import execute
from soda.deploy import deps
execute(deps.install_python_libs)
```


### `deps.install_bower_libs`

Install front-end dependencies from Bower, as defined in the project's
`bower.json`.

```python
from fabric.api import execute
from soda.deploy import deps
execute(deps.install_python_libs)
```


### `django.collectstatic`

Run Django's `collectstatic` management command.

```python
from fabric.api import execute
from soda.deploy import django
execute(django.collectstatic)
```


### `django.migrate`

Run Django's `migrate` management command.

```python
from fabric.api import execute
from soda.deploy import django
execute(django.migrate)
```


### `opbeat.register_deploy`

Register a deployment to the Opbeat integration.

```python
from fabric.api import execute
from soda.deploy import opbeat
execute(opbeat.register_deploy)
```
