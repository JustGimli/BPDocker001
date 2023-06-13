from celery import shared_task
import docker


@shared_task()
def send_message(user_id, message, token="5311611984:AAE49xLBcV5aa9AMdvnm46vna6VFpM3N92Q"):
    client = docker.from_env()

    env_vars = {
        'MESSAGE': message,
        'TOKEN': token,
        'USER_ID': user_id
    }

    client.containers.run('send_message', environment=env_vars, detach=True)

    return f"send_message {message} to {user_id}"
