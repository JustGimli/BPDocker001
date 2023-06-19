from rest_framework.urls import path
from .views import ProgectView


urlpatterns = [
    path('', ProgectView.as_view({'get': 'list'})),
    path('create/', ProgectView.as_view({'post': 'create'})),
    path('delete/', ProgectView.as_view({'post': 'destroy'}))
]
