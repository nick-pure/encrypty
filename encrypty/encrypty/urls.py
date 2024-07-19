from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profiles', include('encprofiles.urls')),
    path('api/messages', include('encmessages.urls')),
]
