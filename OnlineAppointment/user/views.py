from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
import pyotp
from django.contrib import messages
from .models import Appuser
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect('doctor-list')  # Redirect to homepage after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def otp_request_view(request):
    user = request.user
    appuser, created = Appuser.objects.get_or_create(user=user)
    
    if request.method == 'GET':
        if not appuser.otp_secret:
            appuser.otp_secret = pyotp.random_base32()
            appuser.save()
        
        totp = pyotp.TOTP(appuser.otp_secret)
        otp_code = totp.now()
        
        
        print(f"Your OTP code is: {otp_code}")
        
        return render(request, 'otp_verify.html')

    elif request.method == 'POST':
        input_otp = request.POST.get('otp')
        totp = pyotp.TOTP(appuser.otp_secret)
        
        if totp.verify(input_otp):
            messages.success(request, "OTP verified successfully!")
            login(request, user)
            return redirect('doctor-list')  
        else:
            messages.error(request, "Invalid OTP!")
        
    return render(request, 'otp_verify.html')