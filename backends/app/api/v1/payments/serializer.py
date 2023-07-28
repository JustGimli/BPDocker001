from rest_framework import serializers
from apps.payments.models import Self


class SelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Self
        fields = '__all__'
