from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import BotSerializer, BotSettingsSerializer
from rest_framework.response import Response
from apps.users.models import User
from apps.bots.models import Bot, BotSettings
from apps.bots.tasks import run_bot_container


class BotView(viewsets.ModelViewSet):

    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwards):

        id = User.objects.get(email=request.user).id  # request.user
        queryset = Bot.objects.filter(admin=id)

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        run_bot_container.delay(token=serializer.data['token'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BotSettingsView(viewsets.ModelViewSet):
    queryset = BotSettings.objects.select_related(
        'bot__admin', 'bot__name', 'date_update')
    serializer_class = BotSettingsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):

        queryset = BotSettings.objects.filter(bot__admin=request.user)

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
