from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user_logout(request):
    current_user = request.user
    if current_user.is_authenticated:
        logout(request)
        return JsonResponse({"result": "You are now logged out!"})
    else:
        return JsonResponse({"result": "You aren't logged in!"})