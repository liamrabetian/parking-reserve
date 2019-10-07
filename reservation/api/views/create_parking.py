from django.views.decorators.csrf import csrf_exempt
import json
from reservation.models import Floor, ParkingSlot
from django.http import JsonResponse


@csrf_exempt
def create_parking(request): 
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    floor = data.get('floor')
    slots = data.get('slots')
    
    previous_floor = Floor.objects.filter(
        floor_number=floor
    )
    if previous_floor:
        previous_floor.delete()
    f = Floor(floor_number=floor)
    f.save()

    f = Floor.objects.last()
    for slot in slots:
        p = ParkingSlot(floor=f, slot_number=slot)
        p.save()
    return JsonResponse({"result": "parking floor and slots created!"})