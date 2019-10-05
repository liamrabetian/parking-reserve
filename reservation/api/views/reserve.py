import json
from django.http import JsonResponse
from reservation.models import Reservation
from reservation.decorators.validate_params import validate_params
from django.views.decorators.csrf import csrf_exempt
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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
    if current_user.is_authenticated:
        if Reservation.objects.filter(parking_slot=data['parking_slot_id'],
                                        start_date__range=[data['start_date'], data['finish_date']]).exists():
            return JsonResponse({"result": "Dates overlaps. Try other dates and / or parking space."})
        else:
            data['user_id'] = current_user.id
            reserve = Reservation(**data)
            reserve.save()
            return JsonResponse(data={"result": "Reservation done!"})
    else:
        return JsonResponse({"result": "You need to login first!"})
