from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from reservation.models import Reservation, ParkingSlot


# @csrf_exempt
# def available_parkings(request):  
#         available_parkings = Reservation.objects.filter(exit_date__isnull=False).values('parking_slot_id')
#         if available_parkings:
#             return JsonResponse({"result": list(available_parkings)})
#         else:
#             return JsonResponse({"result": "no available parkings at this moment!"})

@csrf_exempt
def available_parkings(request):
    available_parkings = list()
    reserved_parking_slots =  Reservation.objects.all().values_list('parking_slot_id')
    all_parking_slots = ParkingSlot.objects.all().values_list('id')

    for slot in list(all_parking_slots):
        if slot in list(reserved_parking_slots):
             if Reservation.objects.filter(parking_slot_id=slot, exit_date__isnull=False).exists():
                 available_parkings.append(slot)
        else:
            available_parkings.append(slot)
    
    if available_parkings:
        return JsonResponse({"result": available_parkings})
    else:
        return JsonResponse({"result": "no available parkings at this moment!"})




# reserve = Reservation.objects.all().values_list('parking_slot_id')
# reserve = list(reserve)

# parking = ParkingSlot.objects.all().values_list('id')
# parking = list(parking)

# a = list()

# for i in parking:
#     if i in reserve:
#         if Reservation.objects.filter(exit_date__isnull=False).exists():
#             a.append(i)
#     else:
#         a.append(i)



