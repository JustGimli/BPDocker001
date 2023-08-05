from django.urls import path
from .views import BotView, BotSettingsView, BotSettingsApi

urlpatterns = [
    path('create/', BotView.as_view({'post': 'create'})),
    path('message/', BotSettingsApi.as_view()),
    path('delete/<int:id>', BotView.as_view({'get': 'destroy'})),
    path('list/', BotView.as_view({'get': 'list'})),
    path('list/optional/<int:pk>', BotSettingsView.as_view({"get": "list"})),
    path('list/optional/<int:id>', BotSettingsView.as_view({"get": "list"})),
    path('update/<int:pk>/', BotSettingsView.as_view({'patch': 'update'})),
    path('disable/<int:id>', BotSettingsView.as_view({"get": "disable"})),
    path('enable/<int:id>', BotSettingsView.as_view({"get": "enable"})),
    path('reload/<int:id>', BotSettingsView.as_view({"get": "reload"}))
]
