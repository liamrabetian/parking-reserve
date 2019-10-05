from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from reservation.models import Reservation


@csrf_exempt
def available_parkings(request):  
        available_parkings = Reservation.objects.filter(exit_date__isnull=False)
        if available_parkings:
            return JsonResponse({"result": available_parkings})
        else:
            return JsonResponse({"result": "no available parkings at this moment!"})
