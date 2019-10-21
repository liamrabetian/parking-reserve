from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from reservation.models import Reservation
from django.utils import timezone
from reservation.decorators.validate_params import validate_params
from reservation.decorators.login_required import login_required
from reservation.decorators.request_method import check_request_method


schema = {"id": {"type": "integer", "required": True}}


@csrf_exempt
@login_required
@check_request_method(method="PUT")
@validate_params(schema=schema)
def exit_parking(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)
    new_data = dict()
    current_user = request.user

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
