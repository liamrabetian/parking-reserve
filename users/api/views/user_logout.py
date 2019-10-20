from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reservation.decorators.request_method import check_request_method


@csrf_exempt
@check_request_method(method="GET")
def user_logout(request):
    current_user = request.user
    if current_user.is_authenticated:
        logout(request)
        return JsonResponse({"result": "You are now logged out!"}, status=200)
    else:
        return JsonResponse({"result": "You aren't logged in!"}, status=400)
