from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'room', 'start_date', 'end_date',]
        widget = {
            'start_date': forms.TextInput(attrs={type: 'datetime-local'}),
            'end_date': forms.TextInput(attrs={type: 'datetime-local'})
        }
