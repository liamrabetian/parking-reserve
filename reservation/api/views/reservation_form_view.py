from django.shortcuts import render
from django.views import View
from reservation.models import Reservation
from django.db.models import Q

from reservation.forms import ReservationForm


class ReservationView(View):
    def get(self, request):
        reservation = ReservationForm()

        return render(request, 'reservation/index.html', {'form': reservation})

    def post(self, request):
        reservation_form = ReservationForm(data=request.POST)

        if reservation_form.is_valid():
            start_date = reservation_form.cleaned_data['start_date']
            finish_date = reservation_form.cleaned_data['finish_date']
            parking_space_number = reservation_form.cleaned_data['parking_space_number']

            if Reservation.objects.filter(Q(parking_space_number=parking_space_number,
                                            start_date__range=[start_date, finish_date]) |
                                          Q(parking_space_number=parking_space_number,
                                            finish_date__range=[start_date, finish_date])).exists():
                msg = 'Dates overlaps. Try other dates and / or parking space.'
            else:
                msg = 'Reservation taken.'
                reservation_form.save()
                reservation_form = ReservationForm()

            return render(request, 'reservation/index.html', {'message': msg,
                                                              'form': reservation_form})

return render(request, 'reservation/index.html', {'form': reservation_form})