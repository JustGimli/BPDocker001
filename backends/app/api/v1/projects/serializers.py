from rest_framework import serializers

from apps.projects.models import Project, ProjectSettings
from apps.users.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        # unique_together = ['name', 'user']


class ProjectSettingsSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectSettings
        exclude = ['id']

    def create(self, validated_data):
        project_data = validated_data.pop('project', None)
        project_serializer = self.fields['project']


        if project_data:
            project = project_serializer.create(project_data)
            validated_data['project'] = project

        project_settings = ProjectSettings.objects.create(**validated_data)
        return project_settings