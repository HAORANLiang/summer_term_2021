'''import json

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
    sortType = request.GET.get("sortType")
    if sortType == 1:
        list_menu = list_menu.order_by('-start_time')
    elif sortType == 2:
        list_menu = list_menu.order_by('start_time')
    elif sortType == 3:
        list_menu = list_menu.order_by('-create_time')
    elif sortType == 4:
        list_menu = list_menu.order_by('create_time')
    elif sortType == 5:
        list_menu = list_menu.order_by('-list_num')
    elif sortType == 6:
        list_menu = list_menu.order_by('list_num')
    else:
        ret_data = {
            'message': 'sortType error'
        }
        return JsonResponse(ret_data, safe=False)
'''

