# views.py
from django.contrib.auth import get_user_model
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings as djoser_settings
from djoser.utils import ActionViewMixin
from rest_framework import generics, permissions, response, status, views

User = get_user_model()

class ResendActivationView(ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to resend user activation email.
    """
    serializer_class = djoser_settings.SERIALIZERS.password_reset
    permission_classes = [permissions.AllowAny]

    _users = None

    def _action(self, serializer):
        for user in self.get_users(serializer.data['email']):
            self.send_activation_email(user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def get_users(self, email):
        if self._users is None:
            email_field_name = get_user_email_field_name(User)
            self._users = User._default_manager.filter(**{
                email_field_name + '__iexact': email
            })

        return self._users

    def send_activation_email(self, user):
        context = {'user': user}
        to = [get_user_email(user)]
        djoser_settings.EMAIL.activation(self.request, context).send(to)