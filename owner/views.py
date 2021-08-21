import json

from django.http import JsonResponse
from list.models import *
from question.models import *


def get_list(request):
    search_content = request.Get.get("searchContent")
    if len(search_content) == 0:

