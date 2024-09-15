from django.urls import path
from .views import DoctorListView, DoctorDetailView,Add_doctor,Delete_doctor,Edit_doctor

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('adddoctor/',Add_doctor.as_view(),name='adddoctor'),
    path('delete/<int:pk>/', Delete_doctor.as_view(),name='doctor-delete'),
    path('edit/<int:pk>/', Edit_doctor.as_view(),name='doctor-edited'),
]