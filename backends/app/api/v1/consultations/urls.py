from django.urls import path
from .views import  ScenarioViewSet, ConsultationViewSet

urlpatterns = [    
    path('create/',
         ConsultationViewSet.as_view()),
    path('scenario/list/', ScenarioViewSet.as_view({'get': 'list'})),
    path('scenario/redused/', ScenarioViewSet.as_view({'get': 'reduseList'})),
    path('scenario/pk/', ScenarioViewSet.as_view({'get': 'get_by_id'})),
    path('scenario/update/', ScenarioViewSet.as_view({'patch': 'update'})),
    path('scenario/create/', ScenarioViewSet.as_view({'post': 'create'}))
]