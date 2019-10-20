import functools
from django.http import JsonResponse


def login_required(func):
    """Check the user is authenticated or not"""

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"result": "You have to login first!"}, status=401)
        return func(request, *args, *kwargs)

    return wrapper
