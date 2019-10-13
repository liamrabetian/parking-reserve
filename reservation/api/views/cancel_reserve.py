from django.views.decorators.csrf import csrf_exempt
import json
from reservation.models import Reservation
from django.http import JsonResponse
from reservation.decorators.validate_params import validate_params

schema = {"id": {"type": "integer", "required": True}}


@csrf_exempt
@validate_params(schema=schema)
def cancel_reserve(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)

    reservation = data.get("id")
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"result": "You must login first!"})

    try:
        instance = Reservation.objects.filter(
            user_id=current_user.id, id=reservation
        ).first()
        if instance:
            if instance.enter_date:
                return JsonResponse({"result":
                                     "You have already entered the parking!"})
            instance.delete()
            return JsonResponse({"result": "Reservation canceled!"})
        else:
            return JsonResponse({"result": "No such reservation exists!"})
    except Exception:
        return JsonResponse({"result": "Bad Request"})
