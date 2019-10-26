from django.views.decorators.csrf import csrf_exempt
import json
from parking.models import Floor, ParkingSlot
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from reservation.decorators.login_required import login_required
from reservation.decorators.request_method import check_request_method




@csrf_exempt
@login_required
@check_request_method(method="POST")
@permission_required("reservation.admin_role", login_url="/reservation/forbiden_response/", raise_exception=False)
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
            {"result": "These Parking slots already exist!"}, status=403
        )
    return JsonResponse({"result": "parking floor and slots created!"}, status=200)
