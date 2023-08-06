from copy import deepcopy

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from django.db import transaction

from apps.payments.models import IP
from api.v1.payments.serializer import IpSerializer


class IpViewset(viewsets.ModelViewSet):
    serializer_class = IpSerializer
    queryset = IP.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = IP.get_by_user(user=request.user)
        except IP.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IpSerializer(queryset)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        data.update({"user": request.user})

        instance, created = IP.objects.get_or_create(
            user=data.get('user'), defaults=data)

        if not created:
            serializer = self.get_serializer(instance, data=data)
        else:
            serializer = self.get_serializer(instance)

        serializer.is_valid(raise_exception=True)

        if not created:
            self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
