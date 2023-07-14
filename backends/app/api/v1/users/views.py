from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from django.db.models import F

from apps.users.models import User
from apps.payments.models import Account


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = Account.objects.values('balance', 'user__id',
                                              email=F('user__email'), first_name=F('user__first_name'), last_name=F('user__last_name')).get(user=request.user)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialiser = self.get_serializer(queryset)
        return Response(data=serialiser.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
