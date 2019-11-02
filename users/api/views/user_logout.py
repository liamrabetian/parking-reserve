from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reservation.decorators.request_method import check_request_method
from reservation.decorators.login_required import login_required


@csrf_exempt
@login_required
@check_request_method(method="GET")
def user_logout(request):
    logout(request)
    return JsonResponse({"result": "You are now logged out!"}, status=200)
