import json
from django.http import JsonResponse
from reservation.models import Reservation, ParkingSlot
from reservation.decorators.validate_params import validate_params
from django.views.decorators.csrf import csrf_exempt
from .helpers.help_reserve import check_previous_reserve
from django.db.models import Q
from django.utils import timezone


schema = {
    'start_date': {'type': 'string', 'required': True},
    'finish_date': {'type': 'string', 'required': True},
    'parking_slot_id': {'type': ['string', 'integer'], 'required': False}   
}


@csrf_exempt
@validate_params(schema=schema)
def reserve_parking(request):
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    current_user = request.user
    data['user_id'] = current_user.id
    start_date = data.get('start_date')
    finish_date = data.get('finish_date')
    # check the chosen date is valid
    if start_date < str(timezone.now()) or finish_date < str(timezone.now()) or finish_date < start_date:
        return JsonResponse({"result": "Please choose a valid time range!"})
    if not current_user.is_authenticated:
        return JsonResponse({"result": "You need to login first!"}) 
    # reserve the nearest parking slot for the customer if no parking slot is chosen    
    if 'parking_slot_id' not in data:
        # retrieve all parking slots and check if the parking slot is reserved in the next for loop
        reserved_parking_slots =  Reservation.objects.values_list('parking_slot_id', flat=True)
        all_parking_slots = ParkingSlot.objects.values_list('id', flat=True)

        for slot in list(all_parking_slots):
            if slot in list(reserved_parking_slots):
                # check if the parking slot is still reserved or not
                  if Reservation.objects.filter(Q(parking_slot_id=slot, exit_date__isnull=False) | 
                                           Q(parking_slot_id=slot, finish_date__lt=timezone.now())).exists():
                     available_parking = slot
                     break
            else:
                available_parking = slot
                break
        data['parking_slot_id'] = available_parking
        # the function checks if there's already a reservation object with this parking slot in db
        check_previous_reserve(Reservation, data)
        return JsonResponse(data={"result": "Reservation done!"})

    if Reservation.objects.filter(Q(parking_slot_id=data.get('parking_slot_id'),
                                    start_date__range=[start_date, finish_date]) |
                                  Q(parking_slot_id=data.get('parking_slot_id'),
                                    finish_date__range=[start_date, finish_date])).exists():
        return JsonResponse({"result": "Dates overlaps. Try other dates and / or parking space."})
    else:
        check_previous_reserve(Reservation, data)
        return JsonResponse(data={"result": "Reservation done!"})
        
