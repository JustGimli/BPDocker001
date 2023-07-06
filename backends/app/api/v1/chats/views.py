import os
from rest_framework import status, viewsets, generics
from rest_framework.permissions import  AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from apps.chats.models import Message, Chat
from apps.bots.models import Bot
from apps.users.models import User
from .serializers import ChatSerializer, MessageSerializer
from apps.chats.models import BotUsers

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class WebHooks(APIView):
    def post(self, request, format=None):
        chat_obj = request.data.get('id')

        type = request.data.get('type', None)
        if type == 'text':
            text = request.data.get('text')

            message = Message.objects.create(
                text=text,
                is_author=False
            )

            message.save()

            data = message.text

        elif type == 'photo':
            

            message = Message.objects.create(
                photo=request.FILES.get('photo'),
                is_author=False
            )

            message.save()

            data = os.environ.get('URL', "https://botpilot.ru/api") + message.photo.url
        elif type == 'document':
            

            message = Message.objects.create(
                document=request.FILES.get('document'),
                is_author=False
            )

            message.save()
   
            data = os.environ.get('URL', "https://botpilot.ru/api") + message.document.url

        try:
            chat = Chat.objects.get(chat_id=chat_obj)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(
                chat_id=chat_obj,
            )

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
                }
            }
        )

        return Response(status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_400_BAD_REQUEST)


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


class   ChatsViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.select_related(
        'user__first_name', 'user__last_name')
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        token = request.data.get('token')

        if not (username and token):
            return Response(data="need a phone number and token", status=status.HTTP_404_NOT_FOUND)

        try:
            bot = Bot.objects.get(token=token)
        except Bot.DoesNotExist:
            return Response(data="need a bot token", status=status.HTTP_404_NOT_FOUND)

        try:
            user = BotUsers.objects.get(
                username=username, bot=bot.id)
        except BotUsers.DoesNotExist or Bot.DoesNotExist as e:
            print(e)

        
        data = request.data.copy()
        data.update({'user': user.id})

        

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        try:
            chat = Chat.objects.get(chat_id=data.get('chat_id', None))
        except Chat.DoesNotExist:
            print('chat does not exist')
            return Response(status=404)

        chat.expert = bot.admin
        chat.save()



        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):

        queryset = Chat.objects.filter(expert=request.user, is_active=True)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SetCursorPaginations(CursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    ordering = '-time'


class MessageListAPI(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = SetCursorPaginations

    def list(self, request, chat_id,  *args, **kwargs):
        try:
            data = Chat.objects.get(
                chat_id=chat_id)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if data.expert != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(data.messages.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


