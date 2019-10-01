import json
from django.http import JsonResponse
from reservation.models import Reservation
from reservation.decorators.validate_params import validate_params
from django.views.decorators.csrf import csrf_exempt

schema = {
    'start_date': {'type': 'string', 'required': True},
    'finish_date': {'type': 'string', 'required': True},
    'parking_space_number': {'type': 'string', 'required': True}   
}

# for test purpose --> remember to delete
@csrf_exempt
@validate_params(schema=schema)
def reserve_parking(request):
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    if Reservation.objects.filter(parking_space_number=data['parking_space_number'],
                                    start_date__range=[data['start_date'], data['finish_date']]).exists():
        return JsonResponse({"result": "Dates overlaps. Try other dates and / or parking space."})
    else:
        reserve = Reservation(**data)
        reserve.save()
        return JsonResponse(data={"result": "Reservation done!"})
