from rest_framework.urls import path
from .views import ProgectView, ProjectsSettingsViews


urlpatterns = [
    path('create/', ProjectsSettingsViews.as_view({'post': 'create'})),
    path('delete/', ProgectView.as_view({'post': 'destroy'})),
    path('list/full/', ProjectsSettingsViews.as_view({'get': 'list'}))
]
