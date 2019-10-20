from django.views.decorators.csrf import csrf_exempt
import json
from reservation.models import Reservation
from django.http import JsonResponse
from reservation.decorators.validate_params import validate_params
from reservation.decorators.login_required import login_required
from reservation.decorators.request_method import check_request_method


schema = {"id": {"type": "integer", "required": True}}


@csrf_exempt
@login_required
@check_request_method(method="DELETE")
@validate_params(schema=schema)
def cancel_reserve(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)

    reservation = data.get("id")
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"result": "You must login first!"}, status=401)

    try:
        instance = Reservation.objects.get(
            user_id=current_user.id, id=reservation
        )
        if instance.enter_date:
            return JsonResponse({"result":
                                 "You have already entered the parking!"}, status=403)
        instance.delete()
        return JsonResponse({"result": "Reservation canceled!"}, status=200)
    except Exception:
        return JsonResponse({"result": "No such reservation exists!"}, status=404)
