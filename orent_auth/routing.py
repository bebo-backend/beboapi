from django.urls import path, re_path


from orent_auth.consumers import productHubConsumer


websocket_urlpatterns = [
path('ws/upload/<path:username>/', productHubConsumer),
# re_path(r'ws/upload/(?P<username>+)/$', productHubConsumer),
]

