from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication


class SetRefreshTokenMiddleWare(MiddlewareMixin):
    def process_response(self, request, response):

        if response.data:
            if 'refresh' in response.data:

                response.set_cookie(
                    'refresh', response.data['refresh'], httponly=True)

        return response


# class JWTAUTHMiddleware:
#     def __init__(self, inner) -> None:
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#         query =self.scope['query_string']

#         if b'access_token' not query:
#             try:
#                 jwt_auth = JWTAuthentication()
#                 validated_data = jwt_auth.get_validated_token(self.scope['query_string'].decode().split('=')[1])
#                 user = await self.get
