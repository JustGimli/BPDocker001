from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.chats.models import BotUsers
from apps.payment.models import Transaction
from apps.consultations.models import Consultation

from django.utils import timezone
from django.db.models.functions import ExtractDay, ExtractMonth
from django.db.models import Count, F, Sum
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
                users = BotUsers.objects.filter(bot_id__admin_id=expert_id)
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

        data.update({'user': user_id})

        period = request.GET.get('period', False)

        if not period:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif period == "day":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=1)

            return self.get_day(start_date=start_date, end_date=end_date, expert_id=user_id, type='day')
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.get_day(start_date=start_date, end_date=end_date, expert_id=user_id, type='mount')
        elif period == "all time":
            return self.get_day(expert_id=user_id)

        return Response(status=status.HTTP_200_OK)

    def get_day(self, start_date=None, end_date=None, expert_id=None, type=None):

        if start_date and end_date:
            consultations = Consultation.objects.filter(
                start_time__range=(start_date, end_date), expert_id=expert_id).annotate(name=F('scenario__name'))\
                .values('name').annotate(value=Count('name'))
            if type == "month" or type is None:
                try:
                    line = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                        .annotate(month=ExtractMonth('start_time')).values(x=F('month')).annotate(y=Count('id'))
                except Consultation.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                line = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                    .annotate(day=ExtractMonth('start_time')).values(x=F('day')).annotate(y=Count('id'))
        else:
            try:
                consultations = Consultation.objects.filter(
                    expert_id=expert_id).annotate(name=F('scenario__name'))\
                    .values('name').annotate(value=Count('name'))
                line = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                    .annotate(month=ExtractMonth('start_time')).values(x=F('month')).annotate(y=Count('id'))
            except Consultation.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if consultations.exists():

            return Response({
                'pae': consultations,
                'line': line
            }, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PaymentsView(APIView):
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

            return self.get_data(start_date=start_date, end_date=end_date, expert_id=user_id, type="day")
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.get_data(start_date=start_date, end_date=end_date, expert_id=user_id, type="month")
        elif period == "all time":
            return self.get_data(expert_id=user_id)

        return Response(status=status.HTTP_200_OK)

    def get_data(self, start_date=None, end_date=None, expert_id=None, type=None):

        if start_date and end_date:
            try:
                if type == "month" or type is None:
                    transactions = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(month=ExtractMonth('date')).values(x=F('month')).annotate(y=Sum('amount'))

                    transactions_type = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(month=ExtractMonth('date'), name=F('consultation__name'),
                                  sum=Sum('amount')).values('name', type=F('month')).annotate(sum=F('sum'))
                else:
                    transactions = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(day=ExtractDay('date')).values(x=F('day')).annotate(y=Sum('amount'))
                    transactions_type = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(day=ExtractDay('date'), name=F('consultation__name'),
                                  sum=Sum('amount')).values('name', type=F('day')).annotate(sum=F('sum'))

            except Transaction.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                transactions = Transaction.objects.filter(account__user_id=expert_id).annotate(
                    month=ExtractMonth('date')).values(x=F('month')).annotate(y=Sum('amount'))

                transactions_type = Transaction.objects.filter(account__user_id=expert_id)\
                    .annotate(month=ExtractMonth('date'), name=F('consultation__name'),
                              sum=Sum('amount')).values('name', type=F('month')).annotate(sum=F('sum'))
            except Transaction.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if transactions.exists():
            # add check if transaction is secuess
            return Response({'transactions': transactions, "transactions_type": transactions_type}, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):
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

            return self.get_data(start_date=start_date, end_date=end_date, expert_id=user_id, type="day")
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.get_data(start_date=start_date, end_date=end_date, expert_id=user_id, type="month")
        elif period == "all time":
            return self.get_data(expert_id=user_id)

        return Response(status=status.HTTP_200_OK)

    def get_data(self, start_date=None, end_date=None, expert_id=None, type=None):

        if start_date and end_date:
            try:
                users = BotUsers.objects.filter(
                    registration_date__range=(start_date, end_date), bot_id__admin_id=expert_id)
                if type == "month" or type is None:
                    consultations = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                        .annotate(month=ExtractMonth('start_time')).values(x=F('month'))\
                        .annotate(y=Count('id'))
                else:
                    consultations = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                        .annotate(day=ExtractDay('start_time')).values(x=F('day'))\
                        .annotate(y=Count('id'))

            except BotUsers.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                users = BotUsers.objects.filter(bot_id__admin_id=expert_id)
                consultations = Consultation.objects.filter(expert_id=expert_id)\
                    .annotate(day=ExtractMonth('start_time')).values(x=F('day'))\
                    .annotate(y=Count('id'))
            except BotUsers.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if users.exists():
            active_users_count = users.filter(
                is_have_consultation=True).count()
            new_users_count = users.filter(is_have_consultation=False).count()

            return Response({
                'is_have_consultations_count': active_users_count,
                'new_users_count': new_users_count,
                "consultations": consultations
            }, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
