from rest_framework import serializers
from apps.bots.models import Bot
from apps.users.models import User


class BotSerializer(serializers.ModelSerializer):
    # admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Bot
        # fields = '__all__'
        exclude = ['admin', 'date_create']

    def create(self, validated_data):
        validated_data.update({"admin": self.context['request'].user})
        return super().create(validated_data)
