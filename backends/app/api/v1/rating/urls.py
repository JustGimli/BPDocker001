from django.urls import include, path
from .views import RatingView
urlpatterns = [
    path('', RatingView.as_view({'get': 'list'}))
]
