from django.urls import path
from .views import BotView, BotSettingsView, BotSettingsApi

urlpatterns = [
    path('create/', BotView.as_view({'post': 'create'})),
    path('message/',BotSettingsApi.as_view()),
    path('delete/<int:id>', BotView.as_view({'get': 'destroy'})),
    path('list/<str:project_name>/', BotView.as_view({'get': 'list'})),
    path('update/<int:pk>/', BotView.as_view({'patch': 'partial_update'})),
    path('list/optional/<int:pk>', BotSettingsView.as_view({"get": "list"})),
    path('disable/<int:id>', BotSettingsView.as_view({"get": "disable"})),
    path('enable/<int:id>', BotSettingsView.as_view({"get": "enable"}))
]
