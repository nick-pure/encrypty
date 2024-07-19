from django.urls import path

from . import views

app_name = "encprofiles"
urlpatterns = [
    path('create_user', views.create_profile, name='create'),
    path('get_user_by_username/<str:username>', views.get_by_username, name='getByUsername'),
    path('get_user_by_phone/<str:phone>', views.get_by_phone, name='getByPhone'),
    path('get_user/<str:id>', views.get, name='get'),
]