import decimal
import hashlib
from urllib import parse
from urllib.parse import urlparse


def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def parse_response(request: str) -> dict:
    """
    :param request: Link.
    :return: Dictionary.
    """
    params = {}

    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: decimal,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    password: str,  # Merchant password
    **kwargs
) -> bool:
    data = [f'{key}={value}' for key, value in kwargs.items()]
    signature = calculate_signature(
        received_sum, order_number, password, *data)

    if signature.lower() == received_signature.lower():
        return True
    return False


# Формирование URL переадресации пользователя на оплату.

def generate_payment_link(
    merchant_login: str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: decimal,  # Cost of goods, RU
    receipt: dict,
    number: int | str,  # Invoice number
    description: str,  # Description of the purchase
    is_test=0,
    robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx',
    **kwargs
) -> str:
    """URL for redirection of the customer to the service.
    """
    data = [f'{key}={value}' for key, value in kwargs.items()]

    signature = calculate_signature(
        merchant_login,
        cost,
        number,
        receipt,
        merchant_password_1,
        *data
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        "Receipt": receipt,
        'Description': description,
        **kwargs,
        'IsTest': is_test,
        'SignatureValue': signature,
    }
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'


# Получение уведомления об исполнении операции (ResultURL).

def result_payment(merchant_password_2: str, request: str) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    # param_request = parse_response(request)
    cost = request.data.get('OutSum')
    number = request.data.get('InvId')
    signature = request.data.get('SignatureValue')
    shp_id = request.data.get('shp_id')
    shp_name = request.data.get('shp_name')
    shp_userId = request.data.get('shp_userId')
    shp_username = request.data.get('shp_username')
    shp_consultation = request.data.get('shp_consultation')

    if check_signature_result(number, cost, signature, merchant_password_2, shp_consultation=shp_consultation, shp_id=shp_id, shp_name=shp_name, shp_userId=shp_userId, shp_username=shp_username):
        return f'OK{number}',
    return "bad sign"


# Проверка параметров в скрипте завершения операции (SuccessURL).

def check_success_payment(merchant_password_1: str, request: str) -> str:
    """ Verification of operation parameters ("cashier check") in SuccessURL script.
    :param request: HTTP parameters
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    if check_signature_result(number, cost, signature, merchant_password_1):
        return "Thank you for using our service"
    return "bad sign"
