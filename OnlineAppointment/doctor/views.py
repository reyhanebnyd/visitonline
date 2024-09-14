from .models import Doctor, Fulltimes
from .forms import DoctorForm,SearchForm, FilterForm
from datetime import datetime, timedelta, timezone as dt_timezone
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Q


class Add_doctor(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "adddoctor.html"

    def form_valid(self, form):
        # Save the object
        object = form.save()

        # Redirect to the detail view of the created object
        return redirect("doctor-list")



class DoctorListView(ListView):
    model = Doctor
    template_name = "doctor_list.html"
    context_object_name = "doctors"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search form handling
        search_form = SearchForm(self.request.GET)
        if search_form.is_valid():
            search_term = search_form.cleaned_data.get('search_term', '')
            if search_term:
                queryset = queryset.filter(
                    Q(name__icontains=search_term) |
                    Q(career__icontains=search_term)
                )

        # Filter form handling
        filter_form = FilterForm(self.request.GET)
        if filter_form.is_valid():
            pricema = filter_form.cleaned_data.get('pricema')
            pricemi = filter_form.cleaned_data.get('pricemi')
            avg_visit_time = filter_form.cleaned_data.get('avg_visit_time')

            if pricema:
                queryset = queryset.filter(price__lte=pricema)
            if pricemi:
                queryset = queryset.filter(price__gte=pricemi)
            
            if avg_visit_time:
                queryset = queryset.filter(avg_visit_time__gte=avg_visit_time)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['filter_form'] = FilterForm(self.request.GET)
        return context

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctor_detail.html"
    context_object_name = "doctor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object
        doctor1 = self.get_object()
        access_dates = doctor.accessdate

        occupied_times = Fulltimes.objects.filter(id_D=doctor).values_list(
            "accessdate", flat=True
        )
        occupied_times_str = set(occupied_times)

        available_slots = {}
        avg_visit_time = int(doctor.avg_visit_time)

        today = timezone.now().date()
        week_days = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
        }

        for day, times in access_dates.items():
            available_slots[day] = []
            if len(times) == 2:
                start_time_str = times[0]
                end_time_str = times[1]
                start_time = datetime.strptime(start_time_str, "%H:%M").replace(
                    tzinfo=dt_timezone.utc
                )
                end_time = datetime.strptime(end_time_str, "%H:%M").replace(
                    tzinfo=dt_timezone.utc
                )
                # To be refactor
                day_index = list(week_days.keys())[list(week_days.values()).index(day)]
                days_to_add = (day_index - today.weekday() + 7) % 7
                if days_to_add == 0:
                    days_to_add = 7
                appointment_date = today + timedelta(days=days_to_add)
                # -------
                while start_time + timedelta(minutes=avg_visit_time) <= end_time:
                    slot_start = start_time.strftime("%H:%M")
                    slot_end = (
                        start_time + timedelta(minutes=avg_visit_time)
                    ).strftime("%H:%M")

                    full_slot_start_str = datetime.combine(
                        appointment_date, start_time.time()
                    ).isoformat()

                    # What is happening here?
                    full_slot_start_dt = datetime.fromisoformat(
                        full_slot_start_str
                    ).replace(tzinfo=dt_timezone.utc)
                    # Could be replaced with tupel
                    formatted_slot = f"{slot_start} - {slot_end}"

                    # Refactored / If occupied, still add it but mark as booked
                    blocked = full_slot_start_dt in occupied_times_str
                    available_slots[day].append(
                        (formatted_slot, full_slot_start_str, blocked)
                    )

                    start_time += timedelta(minutes=avg_visit_time)

        context["available_slots"] = available_slots
        context["occupied_times"] = occupied_times  # This can be used in the template
        context["doctor"] = doctor1

        return context
