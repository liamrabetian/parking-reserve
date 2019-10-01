from cerberus import Validator
from django.http import JsonResponse

from .cerberus_errors import CustomError

import json


def validate_params(schema, allow_unknown=True):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            try:
                if request.method == 'GET':
                    data = request.GET.dict()
                else:
                    request_body = request.body.decode('utf-8')
                    data = json.loads(request_body)

                v = Validator(schema, error_handler=CustomError, allow_unknown=allow_unknown)
                result = v.validate(data)
            except ValueError:
                res = {'error': 'Bad param format, allowed format: (JSON, URL query)'}
                return JsonResponse(res, status=400)

            if result:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse(v.errors, status=400)

        return wrap

    return decorator
