from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
from .models import Appuser  

class WalletUserSignupForm(UserCreationForm):  
    email = forms.EmailField(required=True)  

    class Meta:  
        model = User  # Change to use the User model directly  
        fields = ('username', 'email', 'password1', 'password2')  

    def save(self, commit=True):  
        user = super().save(commit)  
        # Create the related Appuser instance  
        Appuser.objects.create(user=user)  
        return user