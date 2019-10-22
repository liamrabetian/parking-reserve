from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from reservation.models import Reservation
from parking.models import ParkingSlot
from django.db.models import Q
from django.utils import timezone
from reservation.decorators.validate_params import validate_params
from reservation.decorators.login_required import login_required
from reservation.decorators.request_method import check_request_method


schema = {
    "start_date": {"type": "string", "required": False},
    "finish_date": {"type": "string", "required": False},
}


@csrf_exempt
@login_required
@check_request_method(method="GET")
@validate_params(schema=schema)
def available_parkings(request):
    """User requests to just see which parkings are available right now."""
    available_parkings = list()
    reserved_parking_slots = (
        Reservation.objects.filter(finish_date__gt=timezone.now())
        .select_related("parking_slot")
        .values_list("parking_slot_id", flat=True)
    )
    all_parking_slots = ParkingSlot.objects.values("id", "floor", "slot_number")

    available_parkings = all_parking_slots.exclude(
        id__in=set(reserved_parking_slots)
    )

    if available_parkings.exists():
        return JsonResponse({"result": list(available_parkings)}, status=200)
    else:
        return JsonResponse(
            {"result": "no available parkings at this moment!"}, status=404
        )
