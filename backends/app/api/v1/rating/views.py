from rest_framework import viewsets, status
from apps.rating.models import Rating
from .serializers import RatingSerialisers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class RatingView(viewsets.ViewSet):

    def list(self, request):
        queryset = Rating.objects.all()
        serializer = RatingSerialisers(queryset, many=True)
        return Response(serializer.data)
