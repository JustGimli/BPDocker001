from rest_framework import serializers
from apps.chats.models import BotUsers

from apps.chats.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    phone = serializers.CharField(source='user.phone', required=False)
    params = serializers.JSONField(source='user.params' ,required=False)
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = Chat
        exclude = ['messages']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

