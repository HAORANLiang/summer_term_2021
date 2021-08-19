import json

from django.http import JsonResponse


def plus(request):
    data = json.loads(request.body)
    first = float(data.get("first"))
    second = float(data.get("second"))
    answer = first + second
    ret_data = {
        'answer': answer
    }
    return JsonResponse(ret_data, safe=False)
