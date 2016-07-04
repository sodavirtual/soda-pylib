from fabric.api import env, task


@task
def force():
    """Mark the `force` flag
    """
    env.force = True
