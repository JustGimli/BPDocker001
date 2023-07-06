from .views import  getPaymentsLink, resultPayments
from django.urls import path

urlpatterns = [
    path('result/', resultPayments),
    path('link/', getPaymentsLink)
]