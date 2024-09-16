from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('getusername/', views.get_username_view, name='get_username'),
    path('verify-otp/<str:username>/', views.otp_verify_view, name='otp_verify'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    ]
