from django.urls import path

from . import views

app_name = "encmessages"
urlpatterns = [
    path('create_chat/', views.create_chat, name='create_chat'),
    path('send_text/', views.send_message, name='send_text'),
]