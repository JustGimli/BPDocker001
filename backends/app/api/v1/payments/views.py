import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db import transaction 
from apps.botusers.models import BotUsers
from apps.users.models import User
from apps.bots.models import Bot
from apps.chats.tasks import send_message
from services.robokassa import generate_payment_link, result_payment, check_success_payment

@api_view(['POST'])
def resultPayments(request, *args, **kwargs):
    data = result_payment(os.environ.get('METCHANT_PASSWORD_2'), request)

    if data != 'bad sign':
        with transaction.atomic():
            user = BotUsers.objects.get(username=request.data.get('shp_username'), bot=request.data.get('shp_id'))
            user.is_have_consultation = True
            user.save()
            admin_id = Bot.objects.get(id=request.data.get('shp_id')).admin.id
            admin = User.objects.select_for_update().get(id=admin_id)
            admin.balance += float(request.data.get('OutSum'))
            admin.save()

        token = Bot.objects.get(id=request.data.get('shp_id')).token

        send_message.delay(user_id=request.data.get('shp_userId'), message="Доступ успешно открыт!!!", 
            token=token, name=request.data.get('shp_username'), cons=True, username=request.data.get('shp_username'))
        return Response(data=data, status=status.HTTP_200_OK)
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])        
def getPaymentsLink(request, *args, **kwargs):
    bot_id = request.data.get('id')
    username = request.data.get('username')
    cost = request.data.get('cost')
    description = request.data.get('description', " ")
    user_id = request.data.get('user_id')
    name = request.data.get('name')
        
    if not (bot_id and username and cost and description and user_id and name):
        return Response(data={'error': 'request must contianer a bot token an username in body'}, 
                        status=status.HTTP_400_BAD_REQUEST)

    


    link = generate_payment_link(merchant_login=os.environ.get('MERCHANT_LOGIN'),
        merchant_password_1=os.environ.get('MERCHANT_PASSWORD_1'), cost=cost, description=description, 
        number="", is_test=os.environ.get('ROBOKASSATEST'), shp_id=bot_id, shp_name=name, 
        shp_userId=user_id, shp_username=username)


    return Response(data={'link': link}, status=status.HTTP_200_OK)

