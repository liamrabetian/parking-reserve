from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse


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