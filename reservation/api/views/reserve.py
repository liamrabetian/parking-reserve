import json
from django.http import JsonResponse
from reservation.models import Reservation
from parking.models import ParkingSlot
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .helpers.check_time_validity import check_time_validity
from reservation.decorators.login_required import login_required
from reservation.decorators.request_method import check_request_method




@csrf_exempt
@login_required
@check_request_method(method="POST")
def reserve_parking(request):
    """User can choose a desired parking spot.

    If the spot isn't reserved in the chosen time range,
    the reservation objects will be saved.
    """
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)
    current_user = request.user
    data["user_id"] = current_user.id
    start_date = data.get("start_date")
    finish_date = data.get("finish_date")

    # check the chosen date is valid
    if not check_time_validity(start_date, finish_date):
        return JsonResponse({"result": "Please choose a valid time range!"}, status=400)

    if not ParkingSlot.objects.filter(id=data.get("parking_slot_id")).exists():
        return JsonResponse(
            {"result": "The requested Parking slot doesn't exist!"}, status=400
        )

    if Reservation.objects.filter(
        Q(parking_slot_id=data.get("parking_slot_id"))
        & (
            Q(start_date__range=[start_date, finish_date])
            | Q(finish_date__range=[start_date, finish_date])
        )
    ).exists():
        return JsonResponse(
            {"result": "Dates overlaps. Try other dates and / or parking space."},
            status=403,
        )
    else:
        Reservation(**data).save()
        return JsonResponse(data={"result": "Reservation done!"}, status=200)
