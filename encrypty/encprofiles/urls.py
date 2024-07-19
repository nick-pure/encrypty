from django.urls import path

from . import views

app_name = "encprofiles"
urlpatterns = [
    path('create_user', views.create_user, name='create'),
    path('get_user_by_username/<str:username>', views.get_by_username, name='getByUsername'),
    path('get_user_by_phone/<str:phone>', views.get_by_phone, name='getByPhone'),
    path('get_user_by_id/<str:id>', views.get_by_id, name='getById'),
    path('get_user/<str:arg>', views.get, name='get'),
]