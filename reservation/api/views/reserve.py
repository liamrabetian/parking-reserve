import json
from django.http import JsonResponse
from reservation.models import Reservation
from reservation.decorators.validate_params import validate_params
from django.views.decorators.csrf import csrf_exempt

schema = {
    'start_date': {'type': 'string', 'required': True},
    'finish_date': {'type': 'string', 'required': True},
    'parking_slot_id': {'type': ['string', 'integer'], 'required': True}   
}


@csrf_exempt
@validate_params(schema=schema)
def reserve_parking(request):
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"result": "You need to login first!"}) 
    if Reservation.objects.filter(parking_slot_id=data.get('parking_slot_id'),
                                    start_date__range=[data.get('start_date'), data.get('finish_date')]).exists():
        return JsonResponse({"result": "Dates overlaps. Try other dates and / or parking space."})
    else:
        data['user_id'] = current_user.id
        previous_slot_reserve = Reservation.objects.filter(
            parking_slot_id=data.get('parking_slot_id'),
            start_date=None,
            finish_date=None,
            exit_date__isnull=False
        )
        if previous_slot_reserve:
            data['exit_date'] = None
            previous_slot_reserve.update(**data)
            return JsonResponse(data={"result": "Reservation done!"})
        reserve = Reservation(**data)
        reserve.save()
        return JsonResponse(data={"result": "Reservation done!"})
        
