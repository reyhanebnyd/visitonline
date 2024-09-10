from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Doctor, Fulltimes
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta



class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.all()

  
def timesheet(s, e, a):  
    start_datetime = datetime.combine(datetime.today(), s)  
    end_datetime = datetime.combine(datetime.today(), e)  
    ts = (end_datetime - start_datetime).total_seconds()  
    intervals = []  
    current_time = start_datetime  
    n = int(ts // (a * 60))  
    for _ in range(n):  
        next_time = current_time + timedelta(seconds=a * 60)  
        intervals.append((current_time.time(), next_time.time()))  
        current_time = next_time  
    return intervals  

def doctor_detail(request, doctor_id):  
    # Fetch the doctor, replace Doctor with your model if it's different  
    doctor = get_object_or_404(Doctor, id=doctor_id)  
    
    # Assuming the availability is stored in a JSONField named 'availability'  
    availability = doctor.accessdate  # Adjust this according to your model  

    # Prepare to hold available slots for each day  
    available_slots = {}  
    avg_visit_time = doctor.avg_visit_time
    # Iterate over each day in the availability  
    for day, hours in availability.items():  
        if hours == 'Off':  
            continue  # Skip off days  
        
        # Check if hours is a tuple of time objects  
        if isinstance(hours, tuple) and len(hours) == 2:  
            start_time, end_time = hours  
            if isinstance(start_time, time) and isinstance(end_time, time):  
                available_slots[day] = timesheet(start_time, end_time, avg_visit_time)  
            else:  
                # Handle the case where start_time or end_time is not a time object  
                print(f"Invalid time format for {day}: {hours}")  
        else:  
            print(f"Invalid availability format for {day}: {hours}")  

    # Send the doctor detail and available slots to the template  
    context = {  
        'doctor': doctor,  
        'available_slots': available_slots,  
    }  
    
    return render(request, 'doctor_detail.html', context)