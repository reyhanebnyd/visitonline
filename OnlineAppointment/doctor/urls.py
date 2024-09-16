from django.urls import path
from .views import DoctorListView, DoctorDetailView,Add_doctor, TimeSlotsView

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('adddoctor/',Add_doctor.as_view(),name='adddoctor'),
    path('doctor/<int:doctor_id>/slots/<str:date>/', TimeSlotsView.as_view(), name='time_slots'),
]