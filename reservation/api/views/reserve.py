import json
from django.http import JsonResponse
from reservation.models import Reservation, ParkingSlot
from reservation.decorators.validate_params import validate_params
from django.views.decorators.csrf import csrf_exempt

schema = {
    'start_date': {'type': 'string', 'required': True},
    'finish_date': {'type': 'string', 'required': True},
    'parking_slot_id': {'type': ['string', 'integer'], 'required': False}   
}


def check_previous_reserve(model, data):
    previous_slot_reserve = model.objects.filter(
            parking_slot_id=data.get('parking_slot_id'),
            start_date=None,
            finish_date=None,
            exit_date__isnull=False
        )
    if previous_slot_reserve:
        data['exit_date'] = None
        previous_slot_reserve.update(**data)
        return 
    model(**data).save()

@csrf_exempt
@validate_params(schema=schema)
def reserve_parking(request):
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    current_user = request.user
    data['user_id'] = current_user.id
    if not current_user.is_authenticated:
        return JsonResponse({"result": "You need to login first!"}) 
    if 'parking_slot_id' not in data:
        available_parkings = list()
        reserved_parking_slots =  Reservation.objects.values_list('parking_slot_id', flat=True)
        all_parking_slots = ParkingSlot.objects.values_list('id', flat=True)

        for slot in list(all_parking_slots):
            if slot in list(reserved_parking_slots):
                 if Reservation.objects.filter(parking_slot_id=slot, exit_date__isnull=False).exists():
                     available_parkings.append(slot)
                     break
            else:
                available_parkings.append(slot)
                break
        data['parking_slot_id'] = available_parkings.pop()
        check_previous_reserve(Reservation, data)
        return JsonResponse(data={"result": "Reservation done!"})
    if Reservation.objects.filter(parking_slot_id=data.get('parking_slot_id'),
                                    start_date__range=[data.get('start_date'), data.get('finish_date')]).exists():
        return JsonResponse({"result": "Dates overlaps. Try other dates and / or parking space."})
    else:
        check_previous_reserve(Reservation, data)
        return JsonResponse(data={"result": "Reservation done!"})
        
