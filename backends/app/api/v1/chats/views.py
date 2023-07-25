import os
from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from django.db import transaction
from apps.chats.tasks import send_message
from apps.chats.models import Message, Chat
from apps.bots.models import Bot
from .serializers import ChatSerializer, MessageSerializer
from apps.chats.models import BotUsers

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Subquery, OuterRef, When, Case, Value, CharField


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
                'URL_PATH', "https://botpilot.ru/api") + message.photo.url

            text = f"Вам новое фото на платформе botpilot.ru : {data}"
        elif type == 'document':

            message = Message.objects.create(
                document=request.FILES.get('document'),
                is_author=False,
                is_bot=is_bot
            )

            message.save()

            data = os.environ.get(
                'URL_PATH', "https://botpilot.ru/api") + message.document.url

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


class ChatsViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.select_related(
        'user__first_name', 'user__last_name', 'user__phone', 'user__username', 'user__photo')
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer

    def update(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=request.data.get(
                'chat_id'), expert=request.user)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChatSerializer(chat, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
        chat.is_active = True
        chat.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def list(self, request, *args, **kwargs):
        last_message = Message.objects.filter(
            chat=OuterRef('pk')).annotate(message_type=Case(
                When(text__isnull=False, then=Value('text')),
                When(document__isnull=False, then=Value('document')),
                When(photo__isnull=False, then=Value('photo')),
                When(video__isnull=False, then=Value('video')),
                default=Value('unknown'),
                output_field=CharField())).order_by('-time')[:1]

        queryset = Chat.objects.filter(expert=request.user, is_active=True).annotate(
            last_message_type=Subquery(
                last_message.values('message_type')),
            last_message_text=Subquery(last_message.values(
                'text')), is_author=last_message.values('is_author'), is_bot=last_message.values('is_bot'), time=last_message.values('time'), status=last_message.values('is_read'))

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SetCursorPaginations(CursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    ordering = '-time'


class MessageViewSet(viewsets.ModelViewSet):
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
            paginated_response = self.get_paginated_response(serializer.data)

            # paginated_response['next'] = self.request.build_absolute_uri(
            #     paginated_response['next']).replace('http://', 'https://')
            # paginated_response['previous'] = self.request.build_absolute_uri(
            #     paginated_response['previous']).replace('http://', 'https://')
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        chat_id = request.data.get("chat_id")

        with transaction.atomic():
            serializer = MessageSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            try:
                chat = Chat.objects.get(
                    chat_id=chat_id)
            except Chat.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            chat.messages.add(serializer.data.get('id'))
            chat.save()
            token = chat.user.bot.token
            message = Message.objects.get(id=serializer.data.get('id'))

            serializer = self.get_serializer(message)

            if message.document:
                file = [os.environ.get(
                    "URL_PATH", "https://botpilot.ru/api/")[:-1] + message.document.url]
            elif message.video:
                file = [os.environ.get(
                    "URL_PATH", "https://botpilot.ru/api/")[:-1] + message.video.url]
            else:
                file = [os.environ.get(
                    "URL_PATH", "https://botpilot.ru/api/")[:-1] + message.photo.url]

            send_message.delay(
                user_id=chat_id, message="", token=token, file=file)
            return Response(serializer.data)
