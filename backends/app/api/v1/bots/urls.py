from django.urls import path
from .views import BotView, BotSettingsView

urlpatterns = [
    path('create/', BotView.as_view({'post': 'create'})),
    path('list/<str:project_name>/', BotView.as_view({'get': 'list'})),
    path("status/", BotSettingsView.as_view({"get": "list"})),
    path('update/<int:pk>/', BotView.as_view({'patch': 'partial_update'}))
]
