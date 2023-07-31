from datetime import timedelta, datetime
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.botusers.models import BotUsers
from apps.consultations.models import Consultation, Scenario, File
from django.db.models import F
from django.contrib.postgres.aggregates import ArrayAgg
from apps.users.models import User
from apps.projects.models import Project
from apps.bots.models import Bot
from .serializers import ConsultationSerializer, ScenarioSerializer, ScenarioSerializerRedused
from copy import deepcopy


class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ScenarioSerializerRedused

    def create(self, request, *args, **kwargs):
        user_id = User.objects.get(email=request.user).id

        try:
            bot_id = Bot.objects.get(admin=user_id).id
        except Bot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = deepcopy(request.data)

        try:
            file = data.get('file')
            del data['file']
            file_obj = File.objects.create(file=file)
        except:
            file_obj = None

        data.update({"bot": bot_id})
        if (file_obj):
            data.update({"files":  file_obj.id})

        serializer = ScenarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        user_id = User.objects.get(email=request.user).id

        try:
            queryset = Scenario.objects.filter(bot__admin=user_id)
        except Scenario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ScenarioSerializer(queryset, many=True)
        return Response(serializer.data)

    def reduseList(self, request, *args, **kwargs):
        user_id = User.objects.get(email=request.user).id

        try:
            queryset = Scenario.objects.filter(bot__admin=user_id, is_active=True).values('bot__name', 'bot__date_update', 'bot__id') \
                .annotate(name_list=ArrayAgg('name'))
        except Scenario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_by_id(self, request, *args, **kwargs):
        user_id = User.objects.get(email=request.user).id

        try:
            bot_id = request.query_params.get('bot_id', None)
            bot = Bot.objects.get(id=bot_id, admin=user_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            scenario = Scenario.objects.filter(bot=bot_id)
        except Scenario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ScenarioSerializer(scenario, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_id = User.objects.get(email=request.user).id
        id = request.data.get('scenario_id', None)

        try:
            instance = Scenario.objects.filter(
                bot__admin=user_id, pk=id).first()
        except Scenario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ScenarioSerializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ConsultationCreateApiView(generics.CreateAPIView):
    queryset = Consultation.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ConsultationSerializer

    def create(self, request, *args, **kwargs):
        seconds = float(request.data.get('end_time'))
        end_time = datetime.now() + timedelta(seconds=(seconds))

        try:
            bot = Bot.objects.get(token=request.data.get('token', None))

        except Bot.DoesNotExist:
            text = "expected token"
            return Response(data=text, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get('username', None)

        try:
            user_id = BotUsers.objects.filter(
                username=username, bot_id=bot.id).first().id
        except BotUsers.DoesNotExist:
            text = "user does not exist"
            return Response(data=text, status=status.HTTP_404_NOT_FOUND)

        try:
            expert_id = User.objects.get(id=bot.admin_id).id
        except User.DoesNotExist:
            text = "admin does not exist"
            return Response(data=text, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.update({"user": user_id})
        data.update({"expert": expert_id})
        data.update({"end_time": end_time})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ConsultationViewSet(viewsets.ModelViewSet):
    def list(self, request, user, *args, **kwargs):
        try:
            queryset = Consultation.objects.filter(
                expert=request.user, user_id=user).first()
        except Consultation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConsultationSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)
