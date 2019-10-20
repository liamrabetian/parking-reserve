import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from parking.models import ParkingSlot
from django.contrib.auth.decorators import permission_required
from reservation.decorators.login_required import login_required


@login_required
@permission_required("reservation.admin_role", login_url="/reservation/forbiden_response/", raise_exception=False)
@csrf_exempt
def add_slot(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)
    slots = list(data.get("slots"))
    floor = data.get("floor")

    try:
        ParkingSlot.objects.bulk_create(
            [ParkingSlot(floor_id=floor, slot_number=y) for y in slots]
        )
        return JsonResponse({"result": "Parking Slots added"}, status=200)
    except Exception:
        return JsonResponse(
            {"result": "This floor doesn't exist or these parking slots already exist!"},
            status=400,
        )
