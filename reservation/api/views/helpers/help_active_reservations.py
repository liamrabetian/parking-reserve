from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def forbiden_response(request):
    return JsonResponse({"result": "You don't have admin authority!"}, status=401)
