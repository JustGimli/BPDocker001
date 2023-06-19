from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from django.db.models import Q

from apps.chats.models import Message, Chat, Consultation
from apps.bots.models import Bot
from apps.users.models import User
from .serializers import ChatSerializer, MessageSerializer, BotUsersSerializer, ConsultationSerializer
from apps.chats.models import BotUsers

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class WebHooks(APIView):
    def post(self, request, format=None):
        if request.data.get('message'):
            sender = request.data.get('message', '').get('from', '')
            chat_obj = request.data.get('message', '').get('chat', '')
            text = request.data.get('message', '').get('text', '')

            message = Message.objects.create(
                message=text,
                is_author=False
            )

            message.save()

            try:
                chat = Chat.objects.get(chat_id=chat_obj.get('id', None))
            except Chat.DoesNotExist:
                chat = Chat.objects.create(
                    chat_id=chat_obj.get('id', None),
                )

            chat.messages.add(message)
            chat.save()

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                'group',
                {
                    'type': 'send_data_to_client',
                    'data': {
                        'message_id': message.id,
                        'message_text': message.message,
                        'message_time': str(message.time),

                    }
                }
            )

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class BotInfoHandler(APIView):
    def post(self, request, format=None):
        data = request.data

        print(data)

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
        'user__first_name', 'user__last_name')
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        token = request.data.get('token')

        if not (phone and token):
            return Response(data="need a phone number and token", status=status.HTTP_404_NOT_FOUND)

        try:
            bot_id = Bot.objects.get(token=token).id
        except Bot.DoesNotExist:
            return Response(data="need a bot token", status=status.HTTP_404_NOT_FOUND)

        try:
            user = BotUsers.objects.filter(
                phone=phone, bot=bot_id).first()
        except BotUsers.DoesNotExist or Bot.DoesNotExist as e:
            print(e)

        data = request.data.copy()
        data.update({'user': user.id})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):

        queryset = Chat.objects.filter(expert=request.user)

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


class BotUsersViewSet(generics.CreateAPIView):
    queryset = BotUsers.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BotUsersSerializer

    def create(self, request, *args, **kwargs):
        try:
            bot_id = Bot.objects.get(token=request.data.get('token', None)).id
        except:
            text = "expected token"
            return Response(data=text, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.update({"bot": bot_id})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ConsultationViewSet(generics.CreateAPIView):
    queryset = Consultation.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ConsultationSerializer

    def create(self, request, *args, **kwargs):

        try:
            bot = Bot.objects.get(token=request.data.get('token', None))

        except Bot.DoesNotExist:
            text = "expected token"
            return Response(data=text, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get('username', None)

        try:
            user_id = BotUsers.objects.get(
                Q(username=username) & Q(bot_id=bot.id)).id
        except BotUsers.DoesNotExist:
            text = "user does not exist"
            print(text)
            return Response(data=text, status=status.HTTP_404_NOT_FOUND)

        try:
            expert_id = User.objects.get(id=bot.admin_id).id
        except User.DoesNotExist:
            text = "admin does not exist"
            print(text)
            return Response(data=text, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.update({"user": user_id})
        data.update({"expert": expert_id})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
