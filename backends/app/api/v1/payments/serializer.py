from rest_framework import serializers
from apps.payments.models import Self, IP


class SelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Self
        fields = '__all__'


class IpSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = '__all__'
