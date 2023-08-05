from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.db.models import Subquery, OuterRef, When, Case, Value, CharField
from django.db import transaction

from api.v1.chats.serializers import ChatSerializer

from apps.chats.models import Message, Chat
from apps.bots.models import Bot
from apps.chats.models import BotUsers
from apps.consultations.models import Consultation


class ChatsViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.select_related(
        'user__first_name', 'user__last_name', 'user__phone', 'user__username', 'user__photo', "user__surname")
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer

    def update(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(chat_id=request.data.get(
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

        # consultations = Consultation.objects.filter(expert=request.user)

        queryset = Chat.objects.filter(expert=request.user, is_active=True).annotate(
            last_message_type=Subquery(
                last_message.values('message_type')),
            last_message_text=Subquery(last_message.values(
                'text')), is_author=last_message.values('is_author'), is_bot=last_message.values('is_bot'),
            time=last_message.values('time'), status=last_message.values('is_read'))

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
