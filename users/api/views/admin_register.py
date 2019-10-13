import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login


@csrf_exempt
def admin_register(request):
    request_body = request.body.decode("utf-8")
    data = json.loads(request_body)

    try:
        validate_password(data.get("password"))
    except ValidationError:
        return JsonResponse({"result": "This password is too common!"})

    try:
        user = User.objects.create_user(
            data.get("username"), data.get("email"), data.get("password")
        )
        permission = Permission.objects.get(name="has admin role permissions")
        user.user_permissions.add(permission)
        login(request, user)
        return JsonResponse({"result": "Admin user created"})
    except Exception:
        return JsonResponse({"result": "Username is already taken.choose another!"})
