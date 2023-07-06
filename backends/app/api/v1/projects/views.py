import json
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.models import Project, ProjectSettings
from apps.users.models import User
from .serializers import ProjectSerializer, ProjectSettingsSerializer


class ProgectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        data = request.data

        try:
            id = data.get('id')
        except:
            return Response(data="id is required", status=status.HTTP_404_NOT_FOUND)

        try:
            user_id = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            project = Project.objects.filter(
                id=id, user=user_id).first()
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectsSettingsViews(viewsets.ModelViewSet):
    queryset = ProjectSettings.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSettingsSerializer

    def list(self, request, *args, **kwargs):
        user_id = User.objects.get(email=request.user).id
        queryset = ProjectSettings.objects.filter(project__user=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        try:
            user_id = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            data['project'].update({"user": user_id})
        except:
            error = {"error": "the response must container project object"}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSettingsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)