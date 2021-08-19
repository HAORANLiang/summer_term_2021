import json

from django.http import JsonResponse


def division(request):
    data = json.loads(request.body)
    first = data.get("first")
    second = data.get("second")
    answer = 1.0 * first / second
    ret_data = {
        'answer': answer
    }
    return JsonResponse(ret_data, safe=False)
