from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        max_digits=10, decimal_places=0, required=False)
    user__id = serializers.DecimalField(
        max_digits=10000000000, decimal_places=0, required=False)

    class Meta:
        model = User
        fields = ['user__id', 'email', 'first_name', 'last_name', 'balance']
