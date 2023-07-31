from rest_framework import serializers
from apps.chats.models import BotUsers

from apps.chats.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    last_message_type = serializers.CharField(read_only=True, required=False)
    last_message_text = serializers.CharField(read_only=True, required=False)
    is_author = serializers.BooleanField(required=False)
    is_bot = serializers.BooleanField(required=False)
    time = serializers.DateTimeField(read_only=True, required=False)
    first_name = serializers.CharField(
        source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    phone = serializers.CharField(source='user.phone', required=False)
    params = serializers.JSONField(source='user.params', required=False)
    username = serializers.CharField(source='user.username', required=False)
    photo = serializers.FileField(source='user.photo', required=False)
    surname = serializers.CharField(source='user.surname', required=False)

    class Meta:
        model = Chat
        exclude = ['messages']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
