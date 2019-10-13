from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reservation.models import Reservation
from django.utils import timezone


@csrf_exempt
def user_active_reservations(request):
    current_user = request.user
    reservation = Reservation.objects.filter(
        user_id=current_user.id, finish_date__gt=timezone.now()
    ).values("id", "start_date", "finish_date", "parking_slot", "created_date")

    if reservation:
        return JsonResponse({"result": list(reservation)})
    return JsonResponse({"result": "You have no active reservations"})
