from django.urls import include, path

urlpatterns = [
    path('rating/', include('api.v1.rating.urls')),
    path('bots/', include('api.v1.bots.urls'))
]
