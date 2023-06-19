import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.chats.tasks import send_message
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.chats.models import Chat
from .serializers import MessageSerializer, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            'group',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'group',
            self.channel_name
        )

        print(close_code)

    async def receive(self, text_data):

        data = json.loads(text_data)

        chat_id = data.get('chat_id', None)

        if chat_id is None:
            await self.close()

        access_token = self.scope['query_string'].decode().split('=')[1]

        # Validate the token and retrieve the user
        user = await self.get_user(access_token)

        if user is None:
            # Reject the connection if the token is invalid or the user doesn't exist
            await self.close()
        else:

            message, token = await self.get_chat(chat_id=chat_id, user=user, data=data.get('data', None))

            if message:

                message_data = {
                    "id": message.id,
                    "message": message.message,
                    "is_read": message.is_read,
                    "time": str(message.time),
                    "is_author": message.is_author
                }

                send_message.delay(
                    user_id=chat_id, message=message.message, token=token)

                await self.send(text_data=json.dumps(message_data))
            else:
                await self.close()

    async def send_data_to_client(self, event):

        data = event['data']

        message_data = {
            "id": data.get('message_id'),
            "message": data.get('message_text'),
            "is_read": False,
            "time": data.get('message_time'),
            "is_author": False
        }

        await self.send(text_data=json.dumps(message_data))

    @database_sync_to_async
    def get_user(self, access_token):
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
            return user
        except Exception as e:
            return None

    @database_sync_to_async
    def get_chat(self, chat_id, user, data=None):
        try:
            chat = Chat.objects.get(chat_id=chat_id)
            token = chat.user.bot.token

            if chat.expert != user:
                return None

            serializer = MessageSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            message = Message.objects.create(**serializer.validated_data)
            chat.messages.add(message)

            return message, token

        except (Chat.DoesNotExist, Exception) as e:
            print(e)
            return None