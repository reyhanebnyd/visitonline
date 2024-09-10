from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(),name='user_register'),
    path('log in/',views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view() , name='user_logout'),
]