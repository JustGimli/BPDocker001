from django.urls import path
from .views import ResendActivationView

urlpatterns = [ 
    path('auth/resend-activation/', ResendActivationView.as_view(), name='resend_activation'),
]
