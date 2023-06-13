from django.urls import include, path

urlpatterns = [
    path('rating/', include('api.v1.rating.urls')),
    path('bots/', include('api.v1.bots.urls')),
    path('chats/', include('api.v1.chats.urls')),
    path('projects/', include('api.v1.projects.urls')),
    path('statistics/', include('api.v1.statistic.urls'))
]
