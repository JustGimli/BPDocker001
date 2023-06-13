from rest_framework import serializers
from apps.chats.models import BotUsers

from apps.chats.models import Chat, Message, Consultation


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        exclude = ['user', 'messages', 'bot']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class BotUsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = BotUsers


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Consultation
