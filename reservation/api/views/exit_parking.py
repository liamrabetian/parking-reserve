from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from reservation.models import Reservation
from django.utils import timezone


@csrf_exempt
def exit_parking(request): 
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    new_data = dict()
    parking_slot = data.get('parking_slot_id')
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"result": "you must login first"})

    reserved_parking_slot = Reservation.objects.filter(user_id=current_user.id, 
                                                       parking_slot_id=parking_slot, exit_date__isnull=True)
    if not reserved_parking_slot:
        return JsonResponse({"result": "the parking lot isn't reserved by you!"})  
    new_data['start_date'] = None
    new_data['finish_date'] = None
    new_data['exit_date'] = timezone.now()
    reserved_parking_slot.update(**new_data)                                             
    return JsonResponse({"result": "your exit has been recorded!"})
