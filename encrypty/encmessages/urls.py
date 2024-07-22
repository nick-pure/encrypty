from django.urls import path

from . import views

app_name = "encmessages"
urlpatterns = [
    path('get_chat/', views.get_chat, name='create_chat'),
    path('send_text/', views.send_message, name='send_text'),
]