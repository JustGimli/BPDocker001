from rest_framework import serializers
from apps.botusers.models import BotUsers


class BotUsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = BotUsers


