import os
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction

from .serializers import BotSerializer, BotSettingsSerializer
from rest_framework.response import Response
from apps.users.models import User
from apps.bots.models import Bot, BotSettings
from apps.consultations.models import Scenario
from apps.bots.tasks import run_bot_container, remove_container, stop_container, reload_container


class BotView(viewsets.ModelViewSet):

    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwards):

        queryset = Bot.objects.filter(admin=request.user.id)

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            self.perform_create(serializer)

            primary = Scenario.objects.create(
                name="Первичная консультация", bot=serializer.instance, description="если вы впервые обращаетесь за консультацией")
            secondary = Scenario.objects.create(
                name="Повторная консультация", bot=serializer.instance, description="если ранее вы приходили на очный приём или получали онлайн-консультацию")

            primary.save()
            secondary.save()

        run_bot_container.delay(token=serializer.data['token'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, id,  *args, **kwargs):
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            bot = Bot.objects.get(admin=request.user.id, pk=id)
            container_id = BotSettings.objects.get(
                bot__token=bot.token).container_id
        except Bot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        remove_container.delay(container_id)

        bot.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BotSettingsView(viewsets.ModelViewSet):
    queryset = BotSettings.objects.all()
    serializer_class = BotSettingsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, pk,  *args, **kwargs):
        if not pk:
            return Response(data={"error": "bot id needed"}, status=status.HTTP_400_BAD_REQUEST)

        bot_settings = BotSettings.objects.filter(
            bot__admin=request.user, id=pk).first()

        if bot_settings:

            serializer = self.get_serializer(bot_settings)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def disable(self, request, id,  *args, **kwargs):
        try:
            bot = Bot.objects.get(admin=request.user.id, pk=id)
            settings = BotSettings.objects.get(bot__id=bot.id)
            settings.status = 'pending'
            settings.save()
        except (Bot.DoesNotExist, BotSettings.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        stop_container.delay(token=bot.token)

        return Response(status=status.HTTP_200_OK)

    def enable(self, request, id, *args, **kwargs):
        try:
            bot = Bot.objects.get(admin=request.user.id, pk=id)
        except Bot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        run_bot_container.delay(token=bot.token)

        return Response(status=status.HTTP_200_OK)

    def reload(self, request, id, *args, **kwargs):
        try:
            bot = Bot.objects.get(admin=request.user.id, pk=id)
        except Bot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reload_container.delay(token=bot.token)

        return Response(status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        try:
            instance = BotSettings.objects.get(
                bot_id=pk, bot__admin=request.user)
        except BotSettings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


"""
    this is apt endpoints for bots
"""


class BotSettingsApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            token = request.data.get('token')
        except:
            return Response(data={"error": "need a bot token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = BotSettings.objects.values(
                'bot__img', 'start_message').get(bot__token=token)
        except BotSettings.DoesNotExist:
            return Response(data={"error": "need a valid bot token"}, status=status.HTTP_404_NOT_FOUND)

        if data['bot__img']:
            if os.environ.get('PROD') is not None:
                img_url = request.scheme + "://" + request.get_host() + '/api/media/' + \
                    data['bot__img']
            else:
                img_url = request.scheme + "://" + request.get_host() + '/media/' + \
                    data['bot__img']
        else:
            img_url = ''

        resp = {
            'bot_img': img_url,
            'start_message': data['start_message'],
        }

        return Response(data=resp, status=status.HTTP_200_OK)
