from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Doctor


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.all()


class Doctordetails(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'