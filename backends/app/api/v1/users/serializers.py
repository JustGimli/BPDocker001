from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        max_digits=10, decimal_places=0, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'balance', 'surname', 'phone', 'status']
