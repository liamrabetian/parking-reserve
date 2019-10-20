from reservation.models import Reservation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from reservation.decorators.login_required import login_required
from reservation.decorators.request_method import check_request_method


@csrf_exempt
@login_required
@check_request_method(method="GET")
def user_inactive_reservations(request):
    current_user = request.user
    reservations = Reservation.objects.filter(
        Q(user_id=current_user.id, finish_date__lt=timezone.now())
        | Q(user_id=current_user.id, exit_date__isnull=False)
    ).values("id", "enter_date", "exit_date", "parking_slot", "created_date")
    if reservations.exists():
        return JsonResponse({"result": list(reservations)}, status=200)
    return JsonResponse({"result": "You have no inactive reservations"}, status=404)
