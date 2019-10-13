from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reservation.models import Reservation


@csrf_exempt
def user_active_reservations(request):
    current_user = request.user
    reservation = Reservation.objects.filter(
        user_id=current_user.id, exit_date__isnull=True
    ).values("start_date", "finish_date", "parking_slot")

    if reservation:
        return JsonResponse({"result": list(reservation)})
    return JsonResponse({"result": "You have no active reservations"})
