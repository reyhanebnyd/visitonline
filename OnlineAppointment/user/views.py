from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Appuser
import pyotp
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

def print_otp_in_terminal(user):
    # Assuming user has an OTP secret
    
    otp_secret = user.otp_secret  # Replace with the actual way you store user secrets
    totp = pyotp.TOTP(otp_secret)
    otp_code = totp.now()  # Generate OTP code
    
    # Print OTP code in the terminal
    print(f"Generated OTP for {user.username}: {otp_code}")
    
    return otp_code

otp_dict = {}

# View to handle username input and OTP generation

def get_username_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            appuser = user.appuser  # Get the related Appuser object
            otp_code = appuser.generate_otp()  # Generate OTP using Appuser method
            print(f"Generated OTP for {username}: {otp_code}")  # Print OTP in terminal
            request.session['otp_code'] = otp_code  # Store OTP in session
            request.session['otp_username'] = username
            return redirect('otp_verify', username=username)
        except User.DoesNotExist:
            return render(request, 'get_username.html', {'error': 'Username does not exist'})
    return render(request, 'get_username.html')

# View to handle OTP verification
def otp_verify_view(request, username):
    if request.method == 'POST':
        otp_code = request.POST['otp_code']
        try:
            user = User.objects.get(username=username)
            if request.session['otp_code'] == otp_code:
                login(request, user)  # Log the user in
                return redirect('doctor-list')  # Redirect to main page
            else:
                return render(request, 'otp_verify.html', {'error': 'Invalid OTP', 'username': username})
        except User.DoesNotExist:
            return redirect('get_username')  # In case the username does not exist

    return render(request, 'otp_verify.html', {'username': username})