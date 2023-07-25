import os
import docker
from celery import shared_task

from apps.bots.tasks import check_container_exists
from apps.consultations.models import Scenario


def get_files(token: str, name: str):
    try:
        scenario = Scenario.objects.get(name=name, bot__token=token)
        files = scenario.files.all().first()

        return os.environ.get('URL_PATH', "https://botpilot.ru/api/")[:-1] + files.file.url
    except Scenario.DoesNotExist:
        return ""


@shared_task()
def send_message(user_id, message, token, name=None, cons=False, username=None, scenario_id=None, file=None):
    client = docker.from_env()

    container = check_container_exists(client, 'send_message')

    files_list = ''

    if name is not None:
        files_list = get_files(token, name)
    elif file is not None:
        files_list = file

    env_vars = {
        'MESSAGE': message,
        'TOKEN': token,
        'USER_ID': user_id,
        'FILES': files_list,
        'USERNAME': username,
        'CONS': cons,
        'SCENARIO': scenario_id,
        'URL_PATH': os.environ.get('URL_PATH', "https://botpilot.ru/api/")
    }

    data = {}
    if container:
        if container.status != 'running':
            container.remove()
            data.update(
                {"status1": "find stopped send_message container  and  remove container"})

    client.containers.run('send_message', environment=env_vars, detach=True)

    data.update({'status2': f"send_message {message} to {user_id}"})

    return data, env_vars
