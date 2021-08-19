import json

from django.http import JsonResponse


def division(request):
    first = float(request.GET.get("first"))
    second = float(request.GET.get("second"))
    answer = 1.0 * first / second
    ret_data = {
        'answer': answer
    }
    return JsonResponse(ret_data, safe=False)
