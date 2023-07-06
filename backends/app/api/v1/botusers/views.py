from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.botusers.models import BotUsers
from apps.bots.models import Bot
from .serializers import BotUsersSerializer

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
        return Response( status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
def is_exists(request, *args, **kwargs):
    username = request.data.get('username')

    if username is not None:
        try:
            BotUsers.objects.get(username=username)
            return Response(status=status.HTTP_200_OK)
        except BotUsers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)
