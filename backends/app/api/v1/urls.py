from django.urls import include, path

urlpatterns = [
    path('bots/', include('api.v1.bots.urls')),
    path('chats/', include('api.v1.chats.urls')),
    path('statistics/', include('api.v1.statistic.urls')),
    path('users/', include('api.v1.users.urls')),
    path('consultation/', include('api.v1.consultations.urls')),
    path('botusers/', include('api.v1.botusers.urls')),
    path('', include('api.v1.auth.urls')),
    path('payments/', include('api.v1.payments.urls'))
]
