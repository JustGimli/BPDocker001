from celery import shared_task
import docker


@shared_task()
def run_bot_container(token):
    client = docker.from_env()

    env_vars = {
        "TOKEN": token
    }

    client.containers.run('bot', environment=env_vars, detach=True)
    return 'run'
