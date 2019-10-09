from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from reservation.models import Reservation, ParkingSlot
from django.db.models import Q
from django.utils import timezone
from reservation.decorators.validate_params import validate_params


schema = {
    "start_date": {"type": "string", "required": False},
    "finish_date": {"type": "string", "required": False},
    "parking_slot_id": {"type": "integer", "required": False},
}


@csrf_exempt
@validate_params(schema=schema)
def available_parkings(request):
    """Two ways to see the available parkings.

    User requests to see the available parkings in a time range.
    User requests to just see the available parkings right now.
    """
    available_parkings = list()
    reserved_parking_slots = Reservation.objects.values_list(
        "parking_slot_id", flat=True
    )
    all_parking_slots = ParkingSlot.objects.values_list("id", flat=True)
    # see availbale parkings in the chosen time range
    if request.method == "POST":
        import json

        request_body = request.body.decode("utf-8")
        data = json.loads(request_body)
        start_date = data.get("start_date")
        finish_date = data.get("finish_date")
        for slot in list(all_parking_slots):
            if slot in list(reserved_parking_slots):
                if Reservation.objects.filter(
                    Q(parking_slot_id=slot,
                      start_date__range=[start_date, finish_date])
                    | Q(
                        parking_slot_id=slot,
                        finish_date__range=[start_date, finish_date],
                    )
                ).exists():
                    continue
                else:
                    available_parkings.append(slot)
            else:
                available_parkings.append(slot)
        if available_parkings:
            return JsonResponse({"result": available_parkings})
    for slot in list(all_parking_slots):
        if slot in list(reserved_parking_slots):
            if Reservation.objects.filter(
                Q(parking_slot_id=slot, exit_date__isnull=False)
                | Q(parking_slot_id=slot, finish_date__lt=timezone.now())
            ).exists():
                available_parkings.append(slot)
        else:
            available_parkings.append(slot)

    if available_parkings:
        return JsonResponse({"result": available_parkings})
    else:
        return JsonResponse(
            {"result": "no available parkings at this moment!"})
