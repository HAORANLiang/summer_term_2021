from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.http import JsonResponse
import json


# Create your views here.
def jian(request):

    first = request.GET.get("first")
    second = request.GET.get("second")
    first = int(first)
    second = int(second)
    answer = first - second
    ret_data = {
        'answer': answer
    }
    return JsonResponse(ret_data)


def testdemo(request):
    data = json.loads(request.body)
    name = data.get("name")
    age = int(data.get("age"))
    ret_data = {
        'name': name,
        'age': age+1
    }
    return JsonResponse(ret_data, safe=False)