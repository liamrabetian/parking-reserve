import datetime
from django.forms import ModelForm, DateInput, TextInput, ValidationError
from .models import Reservation


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        # Validating form fields using widgets
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'finish_date': DateInput(attrs={'type': 'date'}),
            'parking_space_number': TextInput(attrs={'pattern': '[1-9]+', 'title': 'Enter a valid parking space number'}),
        }

# Additional custom validator for start_date / finish_date fields
    def clean(self):
        data = self.cleaned_data
        start_date = data['start_date']
        finish_date = data['finish_date']

        if start_date > finish_date:
            raise ValidationError('Wrong start and finish dates.')

        if start_date < datetime.date.today():
            raise ValidationError('Start date in the past.')

        return data


class ParkingSpaceForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['parking_space_number']
        widgets = {
            'parking_space_number': TextInput(attrs={'pattern': '[1-9]+', 'title': 'Enter a valid parking space number'})
}