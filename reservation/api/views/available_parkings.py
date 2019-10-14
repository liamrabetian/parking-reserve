from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from reservation.models import Reservation
from parking.models import ParkingSlot
from django.db.models import Q
from django.utils import timezone
from reservation.decorators.validate_params import validate_params


schema = {
    "start_date": {"type": "string", "required": False},
    "finish_date": {"type": "string", "required": False},
}


@csrf_exempt
@validate_params(schema=schema)
def available_parkings(request):
    """Two ways to see the available parkings.

    User requests to see the available parkings in a time range.
    User requests to just see the available parkings right now.
    """
    available_parkings = list()
    reserved_parking_slots = (
        Reservation.objects.filter(finish_date__gt=timezone.now())
        .select_related("parking_slot")
        .values_list("parking_slot_id", flat=True)
    )
    all_parking_slots = ParkingSlot.objects.values("id", "floor", "slot_number")
    # see availbale parkings in the chosen time range
    if request.method == "POST":
        import json

        request_body = request.body.decode("utf-8")
        data = json.loads(request_body)
        start_date = data.get("start_date")
        finish_date = data.get("finish_date")
        for slot in list(all_parking_slots):
            if slot.get("id") in list(reserved_parking_slots):
                if Reservation.objects.filter(
                    Q(parking_slot_id=slot.get("id"))
                    & (
                        Q(start_date__range=[start_date, finish_date])
                        | Q(finish_date__range=[start_date, finish_date])
                    )
                ).exists():
                    continue
                else:
                    available_parkings.append(slot)
            else:
                available_parkings.append(slot)
        if available_parkings:
            return JsonResponse({"result": available_parkings}, status=200)
        else:
            return JsonResponse(
                {"result": "No parking is available in this time range"},
             status=204)
    for slot in list(all_parking_slots):
        if slot.get("id") not in list(reserved_parking_slots):
            available_parkings.append(slot)
        else:
            continue

    if available_parkings:
        return JsonResponse({"result": list(available_parkings)}, status=200)
    else:
        return JsonResponse({"result": "no available parkings at this moment!"}, status=204)
