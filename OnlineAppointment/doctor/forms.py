from django.forms import ModelForm,TimeInput,TimeField
from .models import Doctor


# For future: add a disable button for disable a day

class DoctorForm(ModelForm):
    # Custom TimeInput with additional attributes
    time_widget = TimeInput(attrs={
        'type': 'time', 
        'min': '05:00',
        'max': '23:30'
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

        jsonh = {}

        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        for day in days_of_week:
            starttime = cleaned_data.get(f'{day}_start')
            endtime = cleaned_data.get(f'{day}_end')
            
            if starttime and endtime:
                print('-----------------------')
                jsonh[day] = (starttime.strftime('%H:%M') , endtime.strftime('%H:%M') )
            else:
                jsonh[day] = 'Off'

        cleaned_data['accessdate'] = jsonh

        return cleaned_data
    def save(self, commit=True):
        doctor = super().save(commit=False)
        doctor.accessdate = self.cleaned_data['accessdate']
        if commit:
            doctor.save()
        return doctor