from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Doctor
from .forms import DoctorForm
import datetime

# Create your views here.
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        doctors = Doctor.objects.filter(name__icontains = searched)
        return render(request, 'searchres.html',{'searched':searched,'doctors':doctors})#
    else:
        return render(request, 'searchres.html',{})

# def timesheet(s,e,a):
#     start_datetime = datetime.datetime.combine(datetime.date.today(), s)
#     end_datetime = datetime.datetime.combine(datetime.date.today(), e)  
#     ts = (end_datetime - start_datetime).total_seconds()
#     intervals = []
#     current_time = start_datetime
#     n=int(ts//(a*60))
#     for _ in range(n):
#         next_time = current_time + datetime.timedelta(seconds=a*60)
#         intervals.append((current_time.time(), next_time.time()))
#         current_time = next_time
#     remaining_seconds = ts - (a *60 * n)
#     return intervals


def is_valid_query(param):
    return param != '' and param is not None

def filter(request):
    qs = Doctor.objects.all()
    career = request.GET.get('career')
    price = request.GET.get('price')
    accessdate = request.GET.get('accessdate')
    avg_visit_time = request.GET.get('avg_visit_time')
    
    if is_valid_query(career):
        qs = qs.filter(name__icontains = career)
    elif is_valid_query(price):
        qs = qs.filter(id = price )
    
    if is_valid_query(accessdate):
        qs = qs.filter(price__lte=accessdate)
    if is_valid_query(avg_visit_time):
        qs = qs.filter(price__gte=avg_visit_time)
    context = {
        'queryset' : qs
    }
    return render(request,'filterres.html',context)
class Add_doctor(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "adddoctor.html"
    # def form_void(self, form):
    #     # Original Values
    #     name = form.cleaned_data['name']
    #     starttime = form.cleaned_data['starttime']
    #     endtime = form.cleaned_data['endtime']
    #     avgtime = form.cleaned_data['avgtime']
    #     # Modified Value
    #     jsontsh = timesheet(starttime,endtime,avgtime)
    #     instance = form.save(commit=False)
    #     instance.accesstime = jsontsh
    #     instance.save()
    #     return super().form_valid(form)
class Doctordetails():
    model = Doctor
    template_name = 'Doctordetails.html'

    def get_queryset(self):
        # Get the list of time ranges from your database
        time_ranges = Doctor.objects.all()

        # Calculate the dates for the table
        today = datetime.date.today()
        dates = [today + datetime.timedelta(days=x) for x in range(7)]

        # Create a list of tuples representing the time ranges and dates
        table_data = []
        for date in dates:
            for time_range in time_ranges:
                table_data.append((date, time_range.accessdate))

        return table_data

# class TimeRangeUpdateView(UpdateView):
#     model = Doctor
#     form_class = TimeRangeForm
#     template_name = 'time_range_form.html'

#     def get_success_url(self):
#         return reverse_lazy('time_range_list')
