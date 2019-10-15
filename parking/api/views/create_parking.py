from django.views.decorators.csrf import csrf_exempt
import json
from parking.models import Floor, ParkingSlot
from django.http import JsonResponse
from reservation.decorators.validate_params import validate_params
from django.contrib.auth.decorators import permission_required


schema = {
    "floor": {"type": "string", "required": True},
    "slots": {"type": "list", "required": True},
}


@permission_required("reservation.admin_role", login_url="/reservation/forbiden_response/", raise_exception=False)
@csrf_exempt
@validate_params(schema=schema)
def create_parking(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)
    floor = data.get("floor")
    slots = list(data.get("slots"))

    previous_floor = Floor.objects.filter(floor_number=floor)
    if previous_floor:
        previous_floor.update(floor_number=floor)
    else:
        f = Floor(floor_number=floor)
        f.save()

    try:
        f = Floor.objects.get(floor_number=floor)
        ParkingSlot.objects.bulk_create(
            [ParkingSlot(floor=f, slot_number=y) for y in slots]
        )
    except Exception:
        return JsonResponse(
            {"result": "These Parking slots already exist!"}, status=406
        )
    return JsonResponse({"result": "parking floor and slots created!"}, status=200)
