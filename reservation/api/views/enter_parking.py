from django.views.decorators.csrf import csrf_exempt
from reservation.models import Reservation
import json
from django.utils import timezone
from django.http import JsonResponse


@csrf_exempt
def enter_parking(request):
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    current_user = request.user
    reserved_parking = Reservation.objects.filter(
        user_id=current_user.id, parking_slot_id=data.get('parking_slot_id'),
        exit_date__isnull=True
    )
    if reserved_parking:
        reserved_parking.update(enter_date=timezone.now())
        return JsonResponse({"result": "your enter has been recorded"})
    return JsonResponse({"result": "you don't have a reservation"})