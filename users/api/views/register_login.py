import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.core.exceptions import ValidationError



@csrf_exempt
def register(request):   
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    try:
        validate_password(data.get('password'))
    except ValidationError:
        return JsonResponse({"result": "This password is too common!"})
    try:    
        user = User.objects.create_user(
            data.get('username'),
            data.get('email'),
            data.get('password')
        )
        login(request, user)
    except Exception:
        return JsonResponse({"result": "Username is already taken.choose another!"})
    return JsonResponse(
        {"result": "User Created"}
    )


@csrf_exempt
def user_login(request):  
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)

    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"result": "you are now logged in!"})
    else:
        return JsonResponse({"result": "Wrong username or password!"})


@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({"result": "You are now logged out!"})