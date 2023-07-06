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
        scenarios = Scenario.objects.filter(bot__token=token, is_active=True).values('name', 'price', 'duration')
    except Scenario.DoesNotExist:
        return {}
    
    res = {}

    for scenario in scenarios:
        res[scenario['name']] = {'cost': scenario['price'], 'days': scenario['duration'].days} 

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


def get_fio_id(token: str) -> str:
    try:
        bot = Bot.objects.get(token=token)
        fio = ' '.join([bot.admin.first_name, bot.admin.last_name])
        return fio, bot.id

    except (User.DoesNotExist):
        return "", bot.id

def get_bot_settings(token: str, data:dict):
    try:
        obj = BotSettings.objects.get(bot__token=token)
        container_id = obj.container_id
        params = obj.params
    except:
        data.update({"error getting container id": "unable to find container_id in bot instance"})

    return params, container_id


@shared_task()
def run_bot_container(token):
    data = {}

    cons = get_consultations(token)
    fio, bot_id = get_fio_id(token)
    params, container_id = get_bot_settings(token, data)

    if params is None:
        params = ''
        
    env_vars = {
        "TOKEN": token,
        "CONSULTATIONS":  json.dumps(cons),
        "FIO": fio, 
        "ID": bot_id,
        "PARAMS": json.dumps(params),
        "URL_PATH": os.environ.get('URL_PATH', 'https://botpilot.ru/api/') 
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
        BotSettings.objects.filter(bot__token=token).update(container_id=container.id, status='running')
    except Exception as e: 
        data.update({'error while update BotSettigs':f"{e}"})
    
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

            data.update({'status': f"successfully deleted container {container_id}"})
        else:
            data.update({"status": f"container with this id {container_id} does not exist in docker"})
    else:
        data.update({'status': f"container with this id {container_id} does not exist in db"})

    return data


@shared_task()
def stop_container(token):
    data = {}

    try:
        container_id = BotSettings.objects.get(bot__token=token).container_id
    except:
        data.update({"error getting container id": "unable to find container_id in bot instance"})

    client = docker.from_env()
    container = check_container_exists(client, container_id)

    if container:
        if container.status == 'running':
            container.stop()
            data.update({'status': f"{container_id} is stopped"})
        
        data.update({'status': f"{container_id} is not running"})
    else:
        data.update({'status': f"{container_id} is not exists"} )

    try:
        BotSettings.objects.filter(bot__token=token).update( status='stopped')
    except: 
        data.update({'error':"dont update bot container id"})

    
    return data



    