from django.shortcuts import render,redirect
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
    def form_valid(self, form):
        # Save the object
        object = form.save()

        # Redirect to the detail view of the created object
        return redirect('adddoctor')

class Doctordetails:
    model = Doctor
    template_name = "Doctordetails.html"

