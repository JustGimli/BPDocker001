import os
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from django.db import transaction
from apps.chats.tasks import send_message
from apps.chats.models import Message, Chat
from api.v1.chats.serializers import MessageSerializer


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

    def update(self, request, *args, **kwargs):

        try:
            instance = Message.objects.get(
                id=request.data.get('message_id'))
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
