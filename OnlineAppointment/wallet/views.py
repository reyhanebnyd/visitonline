from django.shortcuts import render, redirect, get_object_or_404  
from django.core.mail import send_mail  
from django.conf import settings  
from django.contrib import messages  
from doctor.models import Fulltimes, Doctor
from wallet.models import Wallet
from user.models import Appuser
from django.core.exceptions import ObjectDoesNotExist  
from django.contrib.auth.decorators import login_required  
from datetime import datetime
from django.http import HttpResponse
from .forms import AddBalanceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
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
        slot_datetime = datetime.fromisoformat(slot) 
        doctor_id = request.POST.get('doctor_id')  
        doctor = Doctor.objects.get(id=doctor_id)  
        doctor_price = doctor.price  
        
        
        wallet = Wallet.objects.get(id_id=request.user.appuser)  # Adjust based on your Wallet model  
        user_balance = wallet.balance  
        
        if user_balance >= doctor_price:  
              
            reservation = Fulltimes.objects.create(  
                id_U=request.user.appuser,  
                id_D_id=doctor_id,  
                accessdate=slot_datetime,  
            )  
              
            wallet.balance -= doctor_price  
            wallet.save()  

            send_payment_success_email(request.user.email, reservation)  

            return render(request, 'success.html', {'reservation': reservation})  
        else:  
              
            return render(request, 'fail.html', {  
                'message': "Insufficient balance. Please add to your wallet.",  
                'wallet_detail_url': '/wallet/'  
            })  
    return render(request, 'payment.html', {'slot': slot, 'doctor_id': doctor_id})  

def send_payment_success_email(to_email, reservation):  
    subject = 'Payment Confirmation'  
    message = f'Your payment for the appointment on {reservation.accessdate} has been confirmed.\n\nThank you for your reservation!'  
    from_email = settings.DEFAULT_FROM_EMAIL  

    send_mail(subject, message, from_email, [to_email], fail_silently=False)

@login_required
def cancel_reservation(request, reservation_id):
   
    reservation = get_object_or_404(Fulltimes, id=reservation_id, id_U=request.user.appuser)
    
    doctor = get_object_or_404(Doctor, id=reservation.id_D_id)   
    refund_amount = doctor.price  

    wallet = get_object_or_404(Wallet, id_id=request.user.appuser)   

     
    wallet.balance += refund_amount  
    wallet.save()  

    reservation.delete()
    
    
    return redirect('reservation_canceled')     

class WalletDetailView(LoginRequiredMixin, DetailView):  
    model = Wallet  
    template_name = 'wallet_detail.html'  
    context_object_name = 'wallet'  

    def get_object(self, queryset=None):  
         
        wallet, created = Wallet.objects.get_or_create(id=self.request.user.appuser, defaults={'balance': 0.00})  
        return wallet  

    

@login_required  
def add_balance(request):  
     
    wallet = get_object_or_404(Wallet, id=request.user.appuser)  

    if request.method == 'POST':  
        form = AddBalanceForm(request.POST)  
        if form.is_valid():  
            amount = form.cleaned_data['amount']  
            wallet.balance += amount  
            wallet.save()   
            return redirect('wallet_detail')   
    else:  
        form = AddBalanceForm()  

    context = {  
        'form': form,  
        'wallet': wallet,  
    }  
    return render(request, 'add_balance.html', context)   

@login_required  
def reservations_page(request):  
     
    reservations = Fulltimes.objects.filter(id_U=request.user.appuser)  
    
    return render(request, 'reservations.html', {'reservations': reservations})          
