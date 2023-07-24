from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from django.db.models import F
from django.db import transaction

from apps.users.models import User
from apps.payments.models import Account


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = User.objects.select_related('account__balance')\
                .values('first_name', 'last_name', 'surname', 'id', 'email', balance=F('account__balance'))\
                .get(email=request.user)
        except User.DoesNotExist:
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


@api_view(['POST'])
def get_user_profile(request, *args, **kwargs):
    telegram_id = request.data.get('telegram_id')

    try:
        user = User.objects.get(telegram_id=telegram_id)
        return Response(data={
            "fio": f"{user.first_name} {user.last_name} {user.surname}"
        })
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_user(request, *args, **kwargs):
    email = request.data.get('email')
    telegram_id = request.data.get('telegram_id')

    try:
        with transaction.atomic():
            user = User.objects.select_for_update().get(email=email, is_active=True)
            user.telegram_id = telegram_id
            user.save()

        return Response(status=status.HTTP_202_ACCEPTED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
