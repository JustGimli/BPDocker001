from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.chats.models import BotUsers

from django.utils import timezone
from django.db.models.functions import ExtractDay, ExtractMonth
from django.db.models import Count
from datetime import timedelta


class GeneralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = request.data

        try:
            user_id = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data.update({'user': user_id})

        period = request.GET.get('period', False)

        if not period:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif period == "day":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=1)

            return self.get_day(start_date=start_date, end_date=end_date, expert_id=user_id)
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.get_day(start_date=start_date, end_date=end_date, expert_id=user_id)
        elif period == "all time":
            return self.get_day(expert_id=user_id)

        return Response(status=status.HTTP_200_OK)

    def get_day(self, start_date=None, end_date=None, expert_id=None):

        if start_date and end_date:
            try:
                users = BotUsers.objects.filter(
                    registration_date__range=(start_date, end_date), bot_id__admin_id=expert_id)

            except BotUsers.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                users = BotUsers.objects.all()
            except BotUsers.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if users.exists():
            active_users_count = users.filter(
                is_have_consultation=True).count()
            new_users_count = users.filter(is_have_consultation=False).count()

            return Response({
                'active_users_count': active_users_count,
                'new_users_count': new_users_count
            }, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ConsultationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = request.data

        try:
            user_id = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data.update({'expert': user_id})

        period = request.GET.get('period', False)

        if not period:

            return Response(data="period need", status=status.HTTP_400_BAD_REQUEST)
        elif period == "day":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=1)

            return self.get_day(start_date=start_date, end_date=end_date, user_id=user_id)
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.get_day(start_date=start_date, end_date=end_date, user_id=user_id)
        elif period == "all time":
            return self.get_day(user_id=user_id)

    def get_day(self, start_date=None, end_date=None, user_id=None):

        if start_date and end_date:
            try:
                consultation = Consultation.objects.filter(
                    start_time__range=(start_date, end_date), expert_id=user_id)
            except Consultation.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                consultation = Consultation.objects.all()
            except Consultation.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if consultation.exists():
            primary_cons = consultation.filter(
                consultation_type="Первичная консультация").count()
            repeat_cons = consultation.filter(
                consultation_type="Повторная консультация").count()

            if start_date and end_date:
                result = consultation.annotate(
                    period=ExtractDay('start_time')).values('period').annotate(count=Count('id')).order_by('period')
            else:
                result = consultation.annotate(
                    period=ExtractMonth('start_time')).values('period').annotate(count=Count('id')).order_by('period')

            return Response({
                'primary_consultaion': primary_cons,
                'repeat_consultation': repeat_cons,
                'consultations_per': result,
            }, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
