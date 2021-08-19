from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.http import JsonResponse
import json
# Create your views here.
def jian(request):
    data = json.loads(request.body)
    first = data.get("first")
    second = data.get("second")
    first = int(first)
    second = int(second)
    answer = first-second
    ret_data = {
        'answer': answer
    }
    return JsonResponse(ret_data)
