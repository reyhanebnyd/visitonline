from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']  # Only include the username field

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()

        return user

class CustomPasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Only show the current password field if the user has a usable password
        if self.user and not self.user.has_usable_password():
            self.fields['current_password'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check if user has a usable password and validate the current password
        if self.user.has_usable_password() and not self.user.check_password(current_password):
            self.add_error('current_password', 'Current password is incorrect.')

        # Ensure new password and confirm password match
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'The new passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        # Save the new password
        new_password = self.cleaned_data['new_password']
        self.user.set_password(new_password)
        if commit:
            self.user.save()