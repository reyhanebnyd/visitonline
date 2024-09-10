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
    remaining_seconds = ts - (a *60 * n)
    return intervals



class DoctorForm(ModelForm):
    # Add the fields explicitly
    starttime = TimeField(widget=TimeInput(format='%H:%M'), required=True)
    endtime = TimeField(widget=TimeInput(format='%H:%M'), required=True)

    class Meta:
        model = Doctor
        fields = ['name', 'career', 'price', 'avg_visit_time']  # No need to include starttime/endtime here since they are form fields

    def clean(self):
        cleaned_data = super().clean()
        starttime = cleaned_data.get('starttime')
        endtime = cleaned_data.get('endtime')
        avgtime = cleaned_data.get('avg_visit_time')

        if starttime and endtime and avgtime:  
            # Perform your calculations here (e.g., calculate combined_value)
            combined_value = timesheet(starttime, endtime, avgtime)

            # You can store this value in a form-only field or pass it elsewhere
            cleaned_data['combined_field'] = combined_value
        
        return cleaned_data

