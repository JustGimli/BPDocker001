from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer

from apps.users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    def list(self, request, *args, **kwargs):
        queryset = User.objects.get(email=request.user)
        serialiser = self.get_serializer(queryset)
        return Response(data=serialiser.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        user= User.objects.get(email=request.user)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)