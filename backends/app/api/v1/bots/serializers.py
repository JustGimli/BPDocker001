from rest_framework import serializers
from apps.bots.models import Bot, BotSettings
from apps.users.models import User


class BotSerializer(serializers.ModelSerializer):
    start_message = serializers.CharField(max_length=512, required=False)
    params = serializers.JSONField(required=False)
    is_fio = serializers.BooleanField(required=False)
    is_phone = serializers.BooleanField(required=False)

    class Meta:
        model = Bot

        exclude = ['admin', 'date_create']

    def create(self, validated_data):
        data = validated_data.pop('start_message', None)
        params = validated_data.pop('params', None)
        is_fio = validated_data.pop('is_fio', True)
        is_phone = validated_data.pop('is_phone', True)

        validated_data.update({"admin": self.context['request'].user})
        bot = self.Meta.model(**validated_data)
        bot.save()
        BotSettings.objects.create(
            bot=bot, start_message=data, params=params, is_fio=is_fio, is_phone=is_phone)

        return bot


class BotSettingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='bot.name')
    date_update = serializers.DateTimeField(source='bot.date_update')

    class Meta:
        model = BotSettings
        fields = ['name',
                  'date_update', 'id', 'status', 'params', 'is_fio', 'is_phone', 'start_message']

    def create(self, validated_data):
        validated_data.update({"admin": self.context['request'].user})
        return super().create(validated_data)
