import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from reservation.decorators.request_method import check_request_method
from reservation.decorators.login_required import login_required
from reservation.models import Reservation
from parking.models import ParkingSlot


@csrf_exempt
@login_required
@check_request_method(method="POST")
def available_parkings_in_time_range(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)
    start_date = data.get("start_date")
    finish_date = data.get("finish_date")
    reserved_parking_slots = (
        Reservation.objects.filter(finish_date__gt=timezone.now())
        .select_related("parking_slot")
        .values_list("parking_slot_id", flat=True)
    )
    all_parking_slots = ParkingSlot.objects.values("id", "floor", "slot_number")
    not_available_parkings = (
        reserved_parking_slots.filter(
            Q(start_date__range=[start_date, finish_date])
            | Q(finish_date__range=[start_date, finish_date])
        )
    ).values_list("parking_slot__id", flat=True)
    available_parkings = all_parking_slots.exclude(id__in=list(not_available_parkings))
    if available_parkings.exists():
        return JsonResponse({"result": list(available_parkings)}, status=200)
    else:
        return JsonResponse(
            {"result": "No parking is available in this time range"}, status=404
        )
