from rest_framework.urls import path
from .views import GeneralView, ConsultationView, PaymentsView, UserView

urlpatterns = [
    path('general/', GeneralView.as_view()),
    path('consultation/', ConsultationView.as_view()),
    path('payments/', PaymentsView.as_view()),
    path('users/', UserView.as_view()),
]
