from reservation.models import Reservation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def active_reservations(request):
    reservations = Reservation.objects.filter(
        exit_date__isnull=True
    ).values('id', 'created_date', 'start_date', 'finish_date', 'parking_slot', 'user__username')
    if reservations:
        return JsonResponse({"result": list(reservations)})
    return JsonResponse({"result": "There are no reservations right now!"})