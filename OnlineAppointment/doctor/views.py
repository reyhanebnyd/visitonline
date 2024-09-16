from .models import Doctor, Fulltimes, Comment
from user.models import Appuser
from .forms import DoctorForm,SearchForm, FilterForm, CommentForm
from datetime import datetime, timedelta, timezone as dt_timezone
from django.utils import timezone
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.views import View

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

class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = "doctor_detail.html"
    context_object_name = "doctor"
    login_url='/login'

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        doctor = self.get_object()  
        access_dates = doctor.accessdate  

        # Create a list to hold the available days for the next month  
        available_days = []  
        today = timezone.now().date()  

        # Define the range of dates (from today to a month ahead)  
        date_range = [today + timedelta(days=i) for i in range(30)]  

        # Mapping weekdays  
        week_days = {  
            0: "monday",  
            1: "tuesday",  
            2: "wednesday",  
            3: "thursday",  
            4: "friday",  
            5: "saturday",  
            6: "sunday",  
        }  

        # Determine available days for the next month  
        for date in date_range:  
            weekday_name = week_days[date.weekday()]  
            if weekday_name in access_dates and access_dates[weekday_name] != 'Off':  
                available_days.append(date)  

        context['available_days'] = available_days 
        #-------------------------------------------------------
        #this part is to handle comments
        context['comments'] = Comment.objects.filter(doctor=self.object)  

        average_rating = (  
            Comment.objects.filter(doctor=self.object)  
            .aggregate(Avg('rating'))['rating__avg']  
        )  
        context['average_rating'] = average_rating 

        return context

    
    def post(self, request, *args, **kwargs):
        # Manually set the object since we're in a POST request
        self.object = self.get_object()
        has_appointment = Fulltimes.objects.filter(  
        id_U=request.user.appuser,  # Assuming request.user is an instance of Appuser  
        id_D=self.object,    # The doctor object  
        ).exists()  

        if not has_appointment:  
            # If the user does not have an appointment, return an error message  
            context = self.get_context_data()  
            context['comment_form'] = CommentForm(request.POST)  # Show form with errors  
            context['error_message'] = "You must have an appointment with this doctor to leave a comment."  
            return self.render_to_response(context)
        # Process the comment form
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create the comment but don't save it yet
            new_comment = comment_form.save(commit=False)
            new_comment.doctor = self.object
            new_comment.user = request.user  # Assumes user is logged in
            new_comment.save()  # Save the comment

            # Redirect to the same page after submitting the form
            return redirect("doctor-detail", pk=self.object.pk)

        # If the form is invalid, reload the page with form errors
        context = self.get_context_data()
        context['comment_form'] = comment_form  # Show form with errors
        return self.render_to_response(context)


class TimeSlotsView(LoginRequiredMixin, View):  
    login_url = '/login'  

    def get(self, request, doctor_id, date):  
        doctor = get_object_or_404(Doctor, pk=doctor_id)  
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()  

        # Retrieve occupied slots  
        occupied_times = Fulltimes.objects.filter(  
            id_D=doctor,  
            accessdate__date=date_obj  
        ).values_list("accessdate", flat=True)  
        occupied_times_str = set(occupied_times)  

        # Get the weekday to retrieve access times  
        week_days = {  
            0: "monday",  
            1: "tuesday",  
            2: "wednesday",  
            3: "thursday",  
            4: "friday",  
            5: "saturday",  
            6: "sunday",  
        }  
        weekday_name = week_days[date_obj.weekday()]  

        access_dates = doctor.accessdate  
        if weekday_name in access_dates and access_dates[weekday_name] != 'Off':  
            start_time_str, end_time_str = access_dates[weekday_name]  
            start_time = datetime.strptime(start_time_str, "%H:%M").time()  
            end_time = datetime.strptime(end_time_str, "%H:%M").time()  

            # Use the shared method to get available time slots  
            avg_visit_time = doctor.avg_visit_time
            available_time_slots = get_available_time_slots(start_time, end_time, avg_visit_time, occupied_times_str)  

            return render(request, 'time_slots.html', {  
                'doctor': doctor,  
                'date': date_obj,  
                'available_slots': available_time_slots  
            })  
        
        return render(request, 'time_slots.html', {  
            'doctor': doctor,  
            'date': date_obj,  
            'available_slots': []  
        })         

class TimeSlotsView(LoginRequiredMixin, View):  
    login_url = '/login'  

    def get(self, request, doctor_id, date):  
        doctor = get_object_or_404(Doctor, pk=doctor_id)  
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()  

        # Retrieve occupied slots  
        occupied_times = Fulltimes.objects.filter(  
            id_D=doctor,  
            accessdate__date=date_obj  
        ).values_list("accessdate", flat=True)  
        occupied_times_str = set(occupied_times)  

        # Get the weekday to retrieve access times  
        week_days = {  
            0: "monday",  
            1: "tuesday",  
            2: "wednesday",  
            3: "thursday",  
            4: "friday",  
            5: "saturday",  
            6: "sunday",  
        }  
        weekday_name = week_days[date_obj.weekday()]  

        access_dates = doctor.accessdate  
        if weekday_name in access_dates and access_dates[weekday_name] != 'Off':  
            start_time_str, end_time_str = access_dates[weekday_name]  
            start_time = datetime.strptime(start_time_str, "%H:%M").time()  
            end_time = datetime.strptime(end_time_str, "%H:%M").time()  

            # Use the shared method to get available time slots  
            avg_visit_time = doctor.avg_visit_time
            available_time_slots = self.get_available_time_slots(start_time, end_time, avg_visit_time, occupied_times_str)  

            return render(request, 'time_slots.html', {  
                'doctor': doctor,  
                'date': date_obj,  
                'available_slots': available_time_slots  
            })  
        
        return render(request, 'time_slots.html', {  
            'doctor': doctor,  
            'date': date_obj,  
            'available_slots': []  
        })        

    def get_available_time_slots(self, start_time, end_time, avg_visit_time, occupied_times):  
            avg_visit_time = int(avg_visit_time)  
            available_time_slots = []  

            # Start from the start_time until the end_time  
            current_time = datetime.combine(timezone.now().date(), start_time)  
            end_time_dt = datetime.combine(timezone.now().date(), end_time)  

            while current_time + timedelta(minutes=avg_visit_time) <= end_time_dt:  
                slot_start_str = current_time.strftime("%H:%M")  
                slot_end_str = (current_time + timedelta(minutes=avg_visit_time)).strftime("%H:%M")  
                full_slot_start_str = current_time.isoformat()  
                full_slot_start_dt = datetime.fromisoformat(full_slot_start_str).replace(tzinfo=dt_timezone.utc)

                # Mark it as booked if it exists in occupied_times  
                blocked = full_slot_start_dt in occupied_times  
                available_time_slots.append((f"{slot_start_str} - {slot_end_str}", full_slot_start_str, blocked))  

                # Increment the time by the average visit time  
                current_time += timedelta(minutes=avg_visit_time)  

            return available_time_slots            
        