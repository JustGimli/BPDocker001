from .views import getPaymentsLink, resultPayments, SelfViewset
from django.urls import path

urlpatterns = [
    path('result/', resultPayments),
    path('link/', getPaymentsLink),
    path('self/create/', SelfViewset.as_view({"post": "create"})),
    path('self/', SelfViewset.as_view({"get": "list"}))
]
