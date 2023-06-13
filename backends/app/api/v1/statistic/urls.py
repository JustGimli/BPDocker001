from rest_framework.urls import path
from .views import GeneralView, ConsultationView

urlpatterns = [
    path('general/', GeneralView.as_view()),
    path('consultation/', ConsultationView.as_view())
]
