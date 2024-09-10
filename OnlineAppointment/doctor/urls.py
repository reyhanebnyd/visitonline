from django.urls import path
from .views import DoctorListView, doctor_detail

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:doctor_id>/', doctor_detail, name='doctor_detail'),
]