from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.http import JsonResponse
import json


# Create your views here.
def save_result(request):
    data = json.loads(request.body)
