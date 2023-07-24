from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps.botusers.models import BotUsers
from apps.chats.models import Chat
from .serializers import BotUsersSerializer
from django.db import transaction


class BotUsersViewSet(viewsets.ModelViewSet):
    queryset = BotUsers.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BotUsersSerializer
    # parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            Chat.objects.create(
                chat_id=request.data.get('chat_id'),
                user_id=serializer.data.get('id'),
                expert_id=request.data.get('expert_id')
            )

        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def edit(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(chat_id=request.data.get(
                'chat_id'))
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BotUsersSerializer(
            chat.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def is_exists(request, *args, **kwargs):
    username = request.data.get('username')
    token = request.data.get('token')
    if username is not None:
        try:
            BotUsers.objects.get(username=username, bot__token=token)
            return Response(status=status.HTTP_200_OK)
        except BotUsers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)
