from django.urls import path

from . import views

app_name = "encprofiles"
urlpatterns = [
    path('get_user_by_<str:field>', views.get_by_, name='getBy'),
    path('get_user/', views.get, name='get'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('get_my_profile/', views.get_my_profile, name='getMyProfile'),
    path('edit_profile_<str:field>/', views.edit_profile, name='edit_profile'),
    path('check-auth/', views.check_auth, name='check_auth'),
    path('check-auth-not-logged-in/', views.check_auth_not_logged_in, name='check_auth_not_logged_in'),
]