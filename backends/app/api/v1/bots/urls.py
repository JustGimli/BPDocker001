from django.urls import path
from .views import BotView

urlpatterns = [
    path('create/', BotView.as_view({'post': 'create'})),
    path('', BotView.as_view({'get': 'list'})),
    path('update/<int:pk>/', BotView.as_view({'patch': 'partial_update'}))
]
