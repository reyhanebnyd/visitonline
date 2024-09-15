from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

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