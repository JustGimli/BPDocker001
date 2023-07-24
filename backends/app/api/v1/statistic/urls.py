from rest_framework.urls import path
from .views import GeneralView,  StatView

urlpatterns = [
    path('general/', GeneralView.as_view()),
    path('consultation/', StatView.as_view({"get": "get"})),
    path('payments/', StatView.as_view({"get": "get_payments_stat"})),
    path('users/', StatView.as_view({"get": "get_user_stat"})),
]
