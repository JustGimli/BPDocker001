from rest_framework import serializers
from apps.chats.models import BotUsers

from apps.chats.models import Chat, Message, Consultation


class ChatSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = Chat
        exclude = ['messages']


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
