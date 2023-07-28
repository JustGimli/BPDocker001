from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.payments.models import Self
from api.v1.payments.serializer import SelfSerializer


class SelfViewset(viewsets.ModelViewSet):
    serializer_class = SelfSerializer
    queryset = Self.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = Self.get_by_user(user=request.user)
        except Self.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SelfSerializer(queryset)
        return Response(serializer.data)
