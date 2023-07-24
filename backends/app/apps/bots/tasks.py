from celery import shared_task
from apps.users.models import User
from .models import Bot, BotSettings
from apps.consultations.models import Scenario
import docker
from decimal import Decimal
import json
import os


def get_consultations(token: str) -> dict:
    try:
        scenarios = Scenario.objects.filter(
            bot__token=token, is_active=True).values('name', 'price', 'duration', 'id', 'description')
    except Scenario.DoesNotExist:
        return {}

    res = {}

    for scenario in scenarios:
        res[scenario['name']] = {
            'cost': scenario['price'], 'days': scenario['duration'].days,
            "id": scenario['id'], 'description': scenario['description']}

    converted_data = {
        key: {
            subkey: str(value) if isinstance(value, Decimal) else value
            for subkey, value in subdict.items()
        }
        for key, subdict in res.items()
    }

    return converted_data


def check_container_exists(client, container_id=None):
    try:
        # Retrieve the container by name
        container = client.containers.get(container_id)

        return container
    except (docker.errors.NotFound, docker.errors.NullResource):
        return None


def get_fio_id_admin(token: str) -> str:
    try:
        bot = Bot.objects.get(token=token)
        fio = ' '.join([bot.admin.first_name, bot.admin.last_name])
        return fio, bot.id, bot.admin.id

    except (User.DoesNotExist):
        return "", bot.id


def get_bot_settings(token: str, data: dict):
    try:
        obj = BotSettings.objects.get(bot__token=token)
        container_id = obj.container_id
        params = obj.params
        is_fio = obj.is_fio
        is_phone = obj.is_phone
    except:
        data.update(
            {"error getting container id": "unable to find container_id in bot instance"})

    return params, container_id, is_fio, is_phone


@shared_task()
def run_bot_container(token):
    data = {}

    cons = get_consultations(token)
    fio, bot_id, admin_id = get_fio_id_admin(token)
    params, container_id, is_fio, is_phone = get_bot_settings(token, data)

    if params is None:
        params = ''

    env_vars = {
        "TOKEN": token,
        "IS_FIO": int(is_fio),
        "IS_PHONE": int(is_phone),
        "CONSULTATIONS":  json.dumps(cons),
        "FIO": fio,
        "BOT_ID": bot_id,
        "PARAMS": json.dumps(params),
        "URL_PATH": os.environ.get('URL_PATH', 'https://botpilot.ru/api/'),
        "ADMIN_ID": admin_id
    }

    client = docker.from_env()
    container = check_container_exists(client, container_id=container_id)

    if container:
        if container.status == 'running':
            container.stop()

        container.remove()
        data.update({"status": "docker container was stopped and removed"})

    container = client.containers.run('bot', environment=env_vars, detach=True)

    try:
        BotSettings.objects.filter(bot__token=token).update(
            container_id=container.id, status='running')
    except Exception as e:
        data.update({'error while update BotSettigs': f"{e}"})

    data.update({"status": "start docker image"})

    return data


@shared_task()
def remove_container(container_id):
    data = {}

    if container_id:
        client = docker.from_env()
        container = check_container_exists(client, container_id)
        if container:
            if container.status == 'running':
                container.stop()

            container.remove()

            data.update(
                {'status': f"successfully deleted container {container_id}"})
        else:
            data.update(
                {"status": f"container with this id {container_id} does not exist in docker"})
    else:
        data.update(
            {'status': f"container with this id {container_id} does not exist in db"})

    return data


@shared_task()
def stop_container(token):
    data = {}

    try:
        container_id = BotSettings.objects.get(bot__token=token).container_id
    except:
        data.update(
            {"error getting container id": "unable to find container_id in bot instance"})

    client = docker.from_env()
    container = check_container_exists(client, container_id)

    if container:
        if container.status == 'running':
            container.stop()
            data.update({'status': f"{container_id} is stopped"})

        data.update({'status': f"{container_id} is not running"})
    else:
        data.update({'status': f"{container_id} is not exists"})

    try:
        BotSettings.objects.filter(bot__token=token).update(status='stopped')
    except:
        data.update({'error': "dont update bot container id"})

    return data


@shared_task()
def reload_container(token):
    data = {}
    data.update(stop_container(token))
    data.update(run_bot_container(token))

    return data
