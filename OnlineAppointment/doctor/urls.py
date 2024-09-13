from django.urls import path
<<<<<<< HEAD
from .views import DoctorListView, DoctorDetailView,Add_doctor
=======
from .views import DoctorListView, DoctorDetailView
>>>>>>> origin/doctor-reyhane-showlist

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
<<<<<<< HEAD
    path('adddoctor/',Add_doctor.as_view(),name='adddoctor'),
=======
    
>>>>>>> origin/doctor-reyhane-showlist
]