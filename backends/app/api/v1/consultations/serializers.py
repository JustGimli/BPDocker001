from rest_framework import serializers
from apps.consultations.models import Consultation, Scenario


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Consultation


class ScenarioSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Scenario

class ScenarioSerializerRedused(serializers.ModelSerializer):
    bot_name = serializers.CharField(source='bot__name')
    date_update = serializers.DateTimeField(source='bot__date_update')
    name_list = serializers.ListField(child=serializers.CharField())
    bot_id = serializers.ReadOnlyField(source='bot__id')

    class Meta:
        fields = ['name_list',  'date_update', 'bot_name', 'bot_id']
        model = Scenario
        