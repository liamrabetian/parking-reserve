from django.http import JsonResponse
from reservation.models import Reservation


def get_available_parking_lots(request):
    data = Reservation.objects.filter(is_parking_available=True)
    if data:
        return JsonResponse(data)
    else:
        return JsonResponse({"result": "No Parking lot is available!"})