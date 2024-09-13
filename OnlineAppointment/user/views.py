from django.contrib.auth import login
from django.shortcuts import render, redirect

from user.forms import WalletUserSignupForm


def signup_view(request):
    if request.method == 'POST':
        form = WalletUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after sign up
            return redirect('doctor-list')  # Redirect to a home page or another page
    else:
        form = WalletUserSignupForm()
    return render(request, 'signup.html', {'form': form})