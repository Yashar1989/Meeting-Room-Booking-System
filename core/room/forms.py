from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    AVAILABILITY_CHOICES=(
        ('8:00-10:00','8:00-10:00'),
        ('10:00-12:00','10:00-12:00'),
        ('12:00-14:00','12:00-14:00'),
        ('14:00-16:00','14:00-16:00'),
        ('16:00-18:00','16:00-18:00'),
    )
    available_time = forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    class Meta:
        model = Reservation
        fields = ['reserve_date', 'available_time']

        widget = {
            'reserve_date': forms.TextInput(attrs={type: 'datetime-local'}),
        }

