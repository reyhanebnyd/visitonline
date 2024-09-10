from django.forms import ModelForm,TimeInput,TimeField
from .models import Doctor
import datetime

def timesheet(s,e,a):
    start_datetime = datetime.datetime.combine(datetime.date.today(), s)
    end_datetime = datetime.datetime.combine(datetime.date.today(), e)  
    ts = (end_datetime - start_datetime).total_seconds()
    intervals = []
    current_time = start_datetime
    n=int(ts//(a*60))
    for _ in range(n):
        next_time = current_time + datetime.timedelta(seconds=a*60)
        intervals.append((current_time.time(), next_time.time()))
        current_time = next_time
    return intervals


# For future: add a disable button for disable a day
from django.forms import TimeInput

class DoctorForm(ModelForm):
    # Custom TimeInput with additional attributes
    time_widget = TimeInput(attrs={
        'type': 'time', 
        'min': '05:00',
        'max': '23:30',
        'required': 'required'
    })

    # Fields for each day of the week with the custom widget
    saturday_start = TimeField(widget=time_widget, required=False)
    saturday_end = TimeField(widget=time_widget, required=False)
    sunday_start = TimeField(widget=time_widget, required=False)
    sunday_end = TimeField(widget=time_widget, required=False)
    monday_start = TimeField(widget=time_widget, required=False)
    monday_end = TimeField(widget=time_widget, required=False)
    thursday_start = TimeField(widget=time_widget, required=False)
    thursday_end = TimeField(widget=time_widget, required=False)
    wednesday_start = TimeField(widget=time_widget, required=False)
    wednesday_end = TimeField(widget=time_widget, required=False)
    tuesday_start = TimeField(widget=time_widget, required=False)
    tuesday_end = TimeField(widget=time_widget, required=False)
    friday_start = TimeField(widget=time_widget, required=False)
    friday_end = TimeField(widget=time_widget, required=False)

    class Meta:
        model = Doctor
        fields = ['name', 'career', 'price', 'avg_visit_time']  # Doctor fields

    def clean(self):
        cleaned_data = super().clean()
        avgtime = cleaned_data.get('avg_visit_time')

        jsonh = {}

        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        for day in days_of_week:
            starttime = cleaned_data.get(f'{day}_start')
            endtime = cleaned_data.get(f'{day}_end')
            
            if starttime and endtime and avgtime:
                jsonh[day] = timesheet(starttime, endtime, avgtime)

        cleaned_data['accesstime'] = jsonh

        return cleaned_data