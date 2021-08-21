import json

from django.db.models import Q
from django.http import JsonResponse
from list.models import *
from question.models import *


def get_list(request):
    search_content = request.Get.get("searchContent")
    owner_id = request.Get.get("owner_id")
    if len(search_content) == 0:
        list_menu = List.objects.filter(owner_id=owner_id)
    else:
        list_menu = List.objects.filter(
            Q(list_name__contains=search_content) &
            Q(owner_id=owner_id)
        )

