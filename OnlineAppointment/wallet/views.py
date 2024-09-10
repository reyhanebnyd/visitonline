from django.shortcuts import render, redirect  
from django.core.mail import send_mail  
from django.conf import settings  
from django.contrib import messages  
from .models import Fulltimes, Appuser  
from django.core.exceptions import ObjectDoesNotExist  
from django.contrib.auth.decorators import login_required  

@login_required  
def payment_view(request):  
    if request.method == 'GET':  
        slot = request.GET.get('slot')  
        doctor_id = request.GET.get('doctor_id')  
        try:  
            existing_reservation = Fulltimes.objects.get(id_U=request.user.appuser, id_D_id=doctor_id)  
            return render(request, 'already_reserved.html', {'reservation': existing_reservation})  
        except ObjectDoesNotExist:  
            return render(request, 'payment.html', {'slot': slot, 'doctor_id': doctor_id})  

    if request.method == 'POST':  
        slot = request.POST.get('slot')  
        doctor_id = request.POST.get('doctor_id')  
        paid = request.POST.get('paid')  

        if paid:  
            
            reservation = Fulltimes.objects.create(  
                id_U=request.user.appuser.id,  
                id_D_id=doctor_id,  
                accessdate=slot,  
            )  

              
            send_payment_success_email(request.user.email, reservation)  

              
            messages.success(request, 'Payment was successful! A confirmation email has been sent to you.')  
            return redirect('success_page')  

    return render(request, 'payment.html', {'slot': slot, 'doctor_id': doctor_id})  

def send_payment_success_email(to_email, reservation):  
    subject = 'Payment Confirmation'  
    message = f'Your payment for the appointment on {reservation.accessdate} has been confirmed.\n\nThank you for your reservation!'  
    from_email = settings.DEFAULT_FROM_EMAIL  

    send_mail(subject, message, from_email, [to_email], fail_silently=False)