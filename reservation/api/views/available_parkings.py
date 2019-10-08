from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from reservation.models import Reservation, ParkingSlot
from django.db.models import Q
from django.utils import timezone


@csrf_exempt
def available_parkings(request):
    available_parkings = list()
    reserved_parking_slots =  Reservation.objects.values_list('parking_slot_id', flat=True)
    all_parking_slots = ParkingSlot.objects.values_list('id', flat=True)

    for slot in list(all_parking_slots):
        if slot in list(reserved_parking_slots):
             if Reservation.objects.filter(Q(parking_slot_id=slot, exit_date__isnull=False) | 
                                           Q(parking_slot_id=slot, finish_date__lt=timezone.now())).exists():
                 available_parkings.append(slot)
        else:
            available_parkings.append(slot)
    
    if available_parkings:
        return JsonResponse({"result": available_parkings})
    else:
        return JsonResponse({"result": "no available parkings at this moment!"})