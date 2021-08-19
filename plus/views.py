import json

from django.http import JsonResponse


def plus(request):
    first = float(request.GET.get("first"))
    second = float(request.GET.get("second"))
    answer = first + second
    ret_data = {
        'answer': answer
    }
    return JsonResponse(ret_data, safe=False)
