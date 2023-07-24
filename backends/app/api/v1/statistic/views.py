from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.chats.models import BotUsers
from apps.payments.models import Transaction
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
        try:
            if start_date and end_date:
                users = BotUsers.objects.filter(
                    registration_date__range=(start_date, end_date), bot_id__admin_id=expert_id)
            else:
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


class StatView(viewsets.ModelViewSet):
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

            return self.__get_data_consultations(start_date=start_date, end_date=end_date, expert_id=user_id, type='day')
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.__get_data_consultations(start_date=start_date, end_date=end_date, expert_id=user_id, type='month')
        elif period == "all time":
            return self.__get_data_consultations(expert_id=user_id)

        return Response(status=status.HTTP_200_OK)

    def get_payments_stat(self, request, *args, **kwargs):
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

            return self.__get_data_payments(start_date=start_date, end_date=end_date, expert_id=user_id, type="day")
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.__get_data_payments(start_date=start_date, end_date=end_date, expert_id=user_id, type="month")
        elif period == "all time":
            return self.__get_data_payments(expert_id=user_id)

        return Response(status=status.HTTP_200_OK)

    def get_user_stat(self, request, *args, **kwargs):
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

            return self.__get_data_user(start_date=start_date, end_date=end_date, expert_id=user_id, type="day")
        elif period == "month":
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.__get_data_user(start_date=start_date, end_date=end_date, expert_id=user_id, type="month")
        elif period == "all time":
            return self.__get_data_user(expert_id=user_id)

        return Response(status=status.HTTP_200_OK)

    def __get_data_payments(self, start_date=None, end_date=None, expert_id=None, type=None):
        try:
            if start_date and end_date:
                if type == "month":
                    transactions = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(month=ExtractMonth('date')).values(x=F('month')).annotate(y=Sum('amount'))

                    result = self.__line_graph_month(
                        transactions, start_date, end_date)

                    transactions_type = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(month=ExtractMonth('date'), name=F('consultation__name'),
                                  sum=Sum('amount')).values('name', type=F('month')).annotate(sum=F('sum'))
                else:
                    transactions = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(day=ExtractDay('date')).values(x=F('day')).annotate(y=Sum('amount'))

                    result = self.__line_graph_day(
                        transactions, start_date, end_date)

                    transactions_type = Transaction.objects.filter(
                        date__range=(start_date, end_date), account__user_id=expert_id)\
                        .annotate(day=ExtractDay('date'), name=F('consultation__name'),
                                  sum=Sum('amount')).values('name', type=F('day')).annotate(sum=F('sum'))
            else:
                transactions = Transaction.objects.filter(account__user_id=expert_id).annotate(
                    month=ExtractMonth('date')).values(x=F('month')).annotate(y=Sum('amount'))

                result = self.__line_graph_year(transactions)

                transactions_type = Transaction.objects.filter(account__user_id=expert_id)\
                    .annotate(month=ExtractMonth('date'), name=F('consultation__name'),
                              sum=Sum('amount')).values('name', type=F('month')).annotate(sum=F('sum'))

        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if transactions.exists():
            # add check if transaction is secuess
            return Response({'transactions': result, "transactions_type": transactions_type}, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def __get_data_user(self, start_date=None, end_date=None, expert_id=None, type=None):
        try:
            if start_date and end_date:
                users = BotUsers.objects.filter(
                    registration_date__range=(start_date, end_date), bot_id__admin_id=expert_id)
                if type == "month":
                    consultations = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                        .annotate(month=ExtractMonth('start_time')).values(x=F('month'))\
                        .annotate(y=Count('id'))

                    result = self.__line_graph_month(
                        consultations, start_date, end_date)
                else:
                    consultations = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                        .annotate(day=ExtractDay('start_time')).values(x=F('day'))\
                        .annotate(y=Count('id'))

                    result = self.__line_graph_day(
                        consultations, start_date, end_date)
            else:
                users = BotUsers.objects.filter(bot_id__admin_id=expert_id)
                consultations = Consultation.objects.filter(expert_id=expert_id)\
                    .annotate(month=ExtractMonth('start_time')).values(x=F('month'))\
                    .annotate(y=Count('id'))

                result = self.__line_graph_year(consultations)

        except (BotUsers.DoesNotExist, Consultation.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if users.exists():
            active_users_count = users.filter(
                is_have_consultation=True).count()
            new_users_count = users.filter(is_have_consultation=False).count()

            return Response({
                'is_have_consultations_count': active_users_count,
                'new_users_count': new_users_count,
                "consultations": result
            }, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def __get_data_consultations(self, start_date=None, end_date=None, expert_id=None, type=None):
        try:
            if start_date and end_date:
                consultations = Consultation.objects.filter(
                    start_time__range=(start_date, end_date), expert_id=expert_id).annotate(name=F('scenario__name'))\
                    .values('name').annotate(value=Count('name'))

                if type == "month":

                    line = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                        .annotate(month=ExtractMonth('start_time')).values(x=F('month')).annotate(y=Count('id'))

                    result = self.__line_graph_month(
                        line, start_date, end_date)
                else:
                    line = Consultation.objects.filter(start_time__range=(start_date, end_date), expert_id=expert_id)\
                        .annotate(day=ExtractDay('start_time')).values(x=F('day')).annotate(y=Count('id'))

                    result = self.__line_graph_day(line, start_date, end_date)

            else:
                consultations = Consultation.objects.filter(
                    expert_id=expert_id).annotate(name=F('scenario__name'))\
                    .values('name').annotate(value=Count('name'))
                line = Consultation.objects.filter(expert_id=expert_id)\
                    .annotate(month=ExtractMonth('start_time')).values(x=F('month')).annotate(y=Count('id'))

                result = self.__line_graph_year(line)
        except Consultation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if consultations.exists():

            return Response({
                'pae': consultations,
                'line': result
            }, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def __line_graph_day(self, items, start_date, end_date):
        counts = {item['x']: item['y'] for item in items}
        result = []
        current_date = start_date
        while current_date <= end_date:
            count = counts.get(current_date.day, 0)
            result.append(
                {'x': current_date.day, 'y': count})
            current_date += timedelta(days=1)

        return result

    def __line_graph_month(self, items, start_date, end_date):
        months_range = range(start_date.month, end_date.month + 1)

        counts = {item['x']: item['y']
                  for item in items}
        return [{'x': month, 'y': counts.get(month, 0)} for month in months_range]

    def __line_graph_year(self, items):
        counts = {item['x']: item['y'] for item in items}
        return [{'x': month, 'y': counts.get(month, 0)} for month in range(1, 13)]
