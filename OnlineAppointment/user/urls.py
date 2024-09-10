from django.urls import path
from .views import SignUpView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('update/', UserUpdateView.as_view(), name='update_user'),
    path('delete/', UserDeleteView.as_view(), name='delete_user'),
]