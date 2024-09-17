from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Appuser
import pyotp
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add the email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Check if an Appuser already exists for this user
            if not Appuser.objects.filter(user=user).exists():
                # Create an associated Appuser instance
                Appuser.objects.create(user=user, email=user.email)
            
            login(request, user)  # Automatically log in after signup
            return redirect('doctor-list')  # Redirect to the desired page
    else:
        form = CustomUserCreationForm()
    
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

@login_required
def update_user_view(request):
    if request.method == 'POST':
        # Update user information
        user_form = UserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user = user_form.save()
            password_form.save()
            
            # Update session to prevent logout after password change
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')  # Redirect to a profile page or any other page
    else:
        user_form = UserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'update_user.html', {
        'user_form': user_form,
        'password_form': password_form
    })

@login_required
def delete_user_view(request):
    if request.method == 'POST':
        # Delete user account
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully!')
        return redirect('signup')  # Redirect to signup or homepage after deletion

    return render(request, 'delete_user.html')