from celery import shared_task
from .models import BotSettings
import docker


@shared_task()
def run_bot_container(token):
    bot_settings = BotSettings.objects.get(bot_id__token=token)

    client = docker.from_env()

    env_vars = {
        "TOKEN": token,
        "PRIMARY_CON": bot_settings.primary,
        "REPEAT_CON": bot_settings.secondary,
        "START_MESSAGE": bot_settings.start_message,

    }

    client.containers.run('bot', environment=env_vars, detach=True)
    return 'bot running successfully'
 