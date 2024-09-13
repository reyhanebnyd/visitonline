from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Doctor, Fulltimes
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, timezone as dt_timezone
from django.utils import timezone 



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
        doctor1 = self.get_object()
        access_dates = doctor.accessdate  

        occupied_times = Fulltimes.objects.filter(id_D=doctor).values_list('accessdate', flat=True)   
        occupied_times_str = set(occupied_times)

        available_slots = {}  
        avg_visit_time = int(doctor.avg_visit_time)  

        today = timezone.now().date()  
        week_days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}  
        
        for day, times in access_dates.items():  
            available_slots[day] = []  
            if len(times) == 2:  
                start_time_str = times[0]  
                end_time_str = times[1]  
                start_time = datetime.strptime(start_time_str, "%H:%M").replace(tzinfo=dt_timezone.utc)    
                end_time = datetime.strptime(end_time_str, "%H:%M").replace(tzinfo=dt_timezone.utc) 
                
                day_index = list(week_days.keys())[list(week_days.values()).index(day)]  
                days_to_add = (day_index - today.weekday() + 7) % 7  
                if days_to_add == 0:   
                    days_to_add = 7  
                appointment_date = today + timedelta(days=days_to_add)  

                while start_time + timedelta(minutes=avg_visit_time) <= end_time: 
                    slot_start = start_time.strftime("%H:%M")  
                    slot_end = (start_time + timedelta(minutes=avg_visit_time)).strftime("%H:%M") 
        
                    full_slot_start_str = datetime.combine(appointment_date, start_time.time()).isoformat()  
                
                
                    full_slot_start_dt = datetime.fromisoformat(full_slot_start_str).replace(tzinfo=dt_timezone.utc) 
                    #full_slot_end = datetime.combine(appointment_date, (start_time + timedelta(minutes=avg_visit_time)).time()).replace(microsecond=0).isoformat()  
                    formatted_slot = f"{slot_start} - {slot_end}"  
                    
                    if full_slot_start_dt not in occupied_times_str:  
                        available_slots[day].append((formatted_slot, full_slot_start_str))  
                    else:  
                        # If occupied, still add it but mark as booked  
                        available_slots[day].append((formatted_slot, full_slot_start_str, True))  

                    start_time += timedelta(minutes=avg_visit_time)  

        context['available_slots'] = available_slots  
        context['occupied_times'] = occupied_times  # This can be used in the template  
        context['doctor'] = doctor1

        return context  
