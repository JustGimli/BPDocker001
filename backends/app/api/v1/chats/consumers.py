import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.chats.tasks import send_message
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.chats.models import Chat
from .serializers import MessageSerializer, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.get_expert_id()
        await self.channel_layer.group_add(
            self.chat_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name
        )

        print(close_code)

    async def receive(self, text_data):

        data = json.loads(text_data)
        chat_id = data.get('chat', None)

        if chat_id is None:
            await self.close()

        access_token = self.assess_token()

        # Validate the token and retrieve the user
        user = await self.get_user(access_token)

        if user is None:
            # Reject the connection if the token is invalid or the user doesn't exist
            await self.close()
        else:

            message, token = await self.get_chat(chat_id=chat_id, user=user, data=data.get('message', None))

            if message:

                message_data = {
                    "message": {
                        "id": message.id,

                        "is_read": message.is_read,
                        "time": str(message.time),
                        "is_author": message.is_author
                    },
                    "data": message.text,
                    "type": 'text',
                    "chat": chat_id
                }

                send_message.delay(
                    user_id=chat_id, message=message.text, token=token)

                await self.send(text_data=json.dumps(message_data))
            else:
                await self.close()

    async def send_data_to_client(self, event):
        data = event['data']

        message_data = {
            'message': {
                "id": data.get('message_id'),
                "is_read": False,
                "time": data.get('message_time'),
                "is_author": False,
            },
            "data": data.get('data'),
            "type": data.get('message_type'),
            "chat": data.get('chat_id')

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

    def get_expert_id(self):
        return self.scope['query_string'].decode().split('&')[1].split('=')[1]

    def assess_token(self):
        return self.scope['query_string'].decode().split('&')[0].split('=')[1]
