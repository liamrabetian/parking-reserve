import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from reservation.decorators.request_method import check_request_method


@csrf_exempt
@check_request_method(method="POST")
def register(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)
    try:
        validate_password(data.get("password"))
    except ValidationError:
        return JsonResponse({"result": "This password is too common!"}, status=403)
    try:
        user = User.objects.create_user(
            data.get("username"), data.get("email"), data.get("password")
        )
        login(request, user)
    except Exception:
        return JsonResponse({"result": "Username is already taken.choose another!"}, status=403)
    return JsonResponse({"result": "User Created"}, status=200)
