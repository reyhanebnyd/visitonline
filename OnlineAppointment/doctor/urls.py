from django.urls import path
from .views import DoctorListView, DoctorDetailView,Add_doctor

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('adddoctor/',Add_doctor.as_view(),name='adddoctor'),
]