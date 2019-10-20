from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reservation.models import Reservation
from django.utils import timezone
from datetime import timedelta


@csrf_exempt
def user_active_reservations(request):
    current_user = request.user
    reservation = Reservation.objects.filter(
        user_id=current_user.id, finish_date__gt=timezone.now()
    ).values("id", "start_date", "finish_date", "parking_slot", "created_date")

    if reservation.exists():
        reserves = list()
        for reserve in reservation:
            diff_time = reserve.get("finish_date") - timezone.now()
            diff_seconds = int(diff_time.total_seconds())
            diff = str(timedelta(seconds=diff_seconds))
            reserve["time_to_end"] = diff
            reserves.append(reserve)
        return JsonResponse({"result": reserves}, status=200)
    return JsonResponse({"result": "You have no active reservations"}, status=404)
