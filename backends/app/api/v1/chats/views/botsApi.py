import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction

from apps.chats.tasks import send_message
from apps.bots.models import Bot
from apps.chats.models import Message, Chat


class WebHooks(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        chat_obj = request.data.get('id')

        type = request.data.get('type', None)
        is_bot = request.data.get('is_bot', False)

        if type == 'text':
            text = request.data.get('text')

            message = Message.objects.create(
                text=text,
                is_author=False,
                is_bot=is_bot
            )

            message.save()

            data = message.text

            text = f"Вам новое текстовое сообщение на платформе botpilot.ru : {data}"
        elif type == 'photo':

            message = Message.objects.create(
                photo=request.FILES.get('photo'),
                is_author=False,
                is_bot=is_bot
            )

            message.save()

            data = os.environ.get(
                'URL_PATH', "https://botpilot.ru/api/")[:-1] + message.photo.url

            text = f"Вам новое фото на платформе botpilot.ru : {data}"
        elif type == 'document':

            message = Message.objects.create(
                document=request.FILES.get('document'),
                is_author=False,
                is_bot=is_bot
            )

            message.save()

            data = os.environ.get(
                'URL_PATH', "https://botpilot.ru/api/")[:-1] + message.document.url

            text = f"Вам новый файл на платформе botpilot.ru : {data}"

        try:
            chat = Chat.objects.get(chat_id=chat_obj)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        chat.messages.add(message)
        chat.save()

        channel_layer = get_channel_layer()
        try:
            channel_id = 'expert' + str(chat.expert.id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        async_to_sync(channel_layer.group_send)(
            channel_id,
            {
                'type': 'send_data_to_client',
                'data': {
                    'message_id': message.id,
                    'message_type': type,
                    'data': data,
                    'message_time': str(message.time),
                    'chat_id': chat_obj,
                    'is_bot': is_bot
                }
            }
        )
        return Response(status=status.HTTP_200_OK)


class BotInfoHandler(APIView):
    def post(self, request, format=None):
        data = request.data

        if data.get('token', None) is not None:

            try:
                bot = Bot.objects.get(token=data.get('token', None))
            except Bot.DoesNotExist:
                print('bot does not exist')
                return Response(status=404)

            try:
                chat = Chat.objects.get(chat_id=data.get('chat_id', None))
            except Chat.DoesNotExist:
                print('chat does not exist')
                return Response(status=404)

            chat.expert = bot.admin
            # chat.bot = bot
            chat.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
