from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Doctor
from .forms import DoctorForm
import datetime


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


class Doctordetails:
    model = Doctor
    template_name = "Doctordetails.html"

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
