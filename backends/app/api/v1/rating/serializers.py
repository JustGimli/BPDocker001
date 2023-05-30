from rest_framework import serializers
from apps.rating.models import Rating


class RatingSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
