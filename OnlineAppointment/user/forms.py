from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *



class AppuserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Appuser
        fields = ('username', 'created_at', 'is_admin')


class AppuserUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Appuser
        fields = ('username','is_admin')

