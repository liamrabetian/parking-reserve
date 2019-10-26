import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .helpers.check_time_validity import check_time_validity
from parking.models import ParkingSlot
from reservation.models import Reservation
from reservation.decorators.login_required import login_required
from reservation.decorators.request_method import check_request_method




@csrf_exempt
@login_required
@check_request_method(method="POST")
def reserve_nearest_parking(request):
    """The nearest parking slot would be reserved if,

    the user does not provide a parking slot id.
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

    reserved_parking_slots = (
        Reservation.objects.filter(finish_date__gt=timezone.now())
        .select_related("parking_slot")
        .values_list("parking_slot_id", flat=True)
    )
    all_parking_slots = ParkingSlot.objects.values_list("id", flat=True)
    # retrieve the first available parking that isn't reserved now
    available_parking = all_parking_slots.exclude(
        id__in=set(reserved_parking_slots)
    ).first()
    if not available_parking:
        return JsonResponse(
            {"result": "No parking is available for reserve right now!"}, status=404
        )
    data["parking_slot_id"] = available_parking
    Reservation(**data).save()
    return JsonResponse(data={"result": "Reservation done!"}, status=200)
