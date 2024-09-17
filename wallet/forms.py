
from django import forms  

class AddBalanceForm(forms.Form):  
    amount = forms.DecimalField(  
        max_digits=10,  
        decimal_places=2,  
        min_value=0,  
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount to add'}),  
    )