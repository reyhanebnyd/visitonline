from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Doctor, Fulltimes
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta



class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.all()


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object
        access_dates = doctor.accessdate
        occupied_times = Fulltimes.objects.filter(id_D=doctor).values_list('accessdate', flat=True)
        available_slots = {}
        avg_visit_time = int(doctor.avg_visit_time)
        for day, times in access_dates.items():
            available_slots[day] = []
            if len(times) == 2:
                start_time_str = times[0]
                end_time_str = times[1]
                start_time = datetime.strptime(start_time_str, "%H:%M")
                end_time = datetime.strptime(end_time_str, "%H:%M")
                while start_time + timedelta(minutes=avg_visit_time) <= end_time:
                    slot_start = start_time.strftime("%H:%M")
                    slot_end = (start_time + timedelta(minutes=avg_visit_time)).strftime("%H:%M")
                    if slot_start not in occupied_times:
                        available_slots[day].append(f"{slot_start} - {slot_end}")

                    start_time += timedelta(minutes=avg_visit_time)

        context['available_slots'] = available_slots

        return context