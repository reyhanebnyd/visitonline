from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView ,ListView, DetailView
from .models import Doctor, Fulltimes
from .forms import DoctorForm
from datetime import datetime, timedelta




# Create your views here.
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        doctors = Doctor.objects.filter(name__icontains=searched)
        return render(
            request, "searchres.html", {"searched": searched, "doctors": doctors}
        )  #
    else:
        return render(request, "searchres.html", {})


def is_valid_query(param):
    return param != "" and param is not None


def filter(request):
    qs = Doctor.objects.all()
    career = request.GET.get("career")
    price = request.GET.get("price")
    accessdate = request.GET.get("accessdate")
    avg_visit_time = request.GET.get("avg_visit_time")

    if is_valid_query(career):
        qs = qs.filter(name__icontains=career)
    elif is_valid_query(price):
        qs = qs.filter(id=price)

    if is_valid_query(accessdate):
        qs = qs.filter(price__lte=accessdate)
    if is_valid_query(avg_visit_time):
        qs = qs.filter(price__gte=avg_visit_time)
    context = {"queryset": qs}
    return render(request, "filterres.html", context)


class Add_doctor(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "adddoctor.html"
    def form_valid(self, form):
        # Save the object
        object = form.save()

        # Redirect to the detail view of the created object
        return redirect('doctor-list')

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

