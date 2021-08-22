import json

from django.db.models import Q
from django.http import JsonResponse
from list.models import *
from list.serializer import ListSerializer
from django.core.paginator import Paginator
from question.models import *


def get_list(request):
    search_content = request.Get.get("searchContent")
    owner_id = request.Get.get("owner_id")
    sortType = request.GET.get("sortType")
    if sortType == 0:
        list_menu = List.objects.filter(owner_id=owner_id)
        all_set = ListSerializer(list_menu, many=True)
        return JsonResponse(all_set.data, safe=False)
    if len(search_content) == 0:
        list_menu = List.objects.filter(owner_id=owner_id)
    else:
        list_menu = List.objects.filter(
            Q(list_name__contains=search_content) &
            Q(owner_id=owner_id)
        )
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
    num_one_page = 5
    paginator = Paginator(list_menu, num_one_page)
    current_page = request.GET.get("currentPage")
    page_current = paginator.page(current_page)
    ret_data = {

    }
