from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
import pyotp
from django.shortcuts import get_object_or_404
from datetime import datetime
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

def otp_view(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until= request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    return redirect('doctor-list')
                else:
                    messages.error(request , 'invalid one time password' , 'warning')
            else:
                messages.error(request , 'one time password has expired' , 'warning')
        else:
            messages.error(request , 'some thing went wrong' , 'warning')    
    return render(request, 'otp.html')
