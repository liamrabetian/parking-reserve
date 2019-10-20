from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from reservation.models import Reservation
from django.utils import timezone
from reservation.decorators.validate_params import validate_params


schema = {"id": {"type": "integer", "required": True}}


@csrf_exempt
@validate_params(schema=schema)
def exit_parking(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)
    new_data = dict()
    current_user = request.user
    if not current_user.is_authenticated:
        return JsonResponse({"result": "you must login first"}, status=401)

    reserved_parking_slot = Reservation.objects.filter(
        user_id=current_user.id, id=data.get("id"),
        exit_date__isnull=True,
        enter_date__isnull=False
    )
    if not reserved_parking_slot.exists():
        return JsonResponse(
            {"result": "the parking lot isn't occupied by you!"}, status=404)
    new_data["start_date"] = None
    new_data["finish_date"] = None
    new_data["exit_date"] = timezone.now()
    reserved_parking_slot.update(**new_data)
    return JsonResponse({"result": "your exit has been recorded!"}, status=200)
