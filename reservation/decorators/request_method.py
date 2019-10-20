from django.http import JsonResponse


def check_request_method(method: str):
    """Check the request method is what you want"""

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not request.method == method:
                return JsonResponse({"result": "The requested method is not allowed"}, status=405)
            return func(request, *args, **kwargs)
        return wrapper

    return decorator
