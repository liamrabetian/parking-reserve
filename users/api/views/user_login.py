from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from reservation.decorators.request_method import check_request_method


@csrf_exempt
@check_request_method(method="POST")
def user_login(request):
    if request.user.is_authenticated:
        return JsonResponse({"result": "You are ALREADY logged in!"}, status=200)
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)

    username = data.get("username")
    password = data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"result": "you are now logged in!"}, status=200)
    else:
        return JsonResponse({"result": "Wrong username or password!"}, status=401)
