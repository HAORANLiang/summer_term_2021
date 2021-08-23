import json

from django.db.models import Q
from django.http import JsonResponse
from list.models import *
from owner.models import *
from list.serializer import ListSerializer
from django.core.paginator import Paginator
from question.models import *


def get_list(request):
    search_content = request.GET.get("searchContent")
    owner_id = int(request.GET.get("owner_id"))
    sortType = int(request.GET.get("sortType"))
    if sortType == 0:
        list_menu = List.objects.filter(owner_id=owner_id)
        all_set = ListSerializer(list_menu, many=True)
        return JsonResponse(all_set.data, safe=False)
    if search_content is None:
        list_menu = List.objects.filter(owner_id=owner_id)
        list_menu = list_menu.exclude(state="已删除")
    else:
        list_menu = List.objects.filter(
            Q(list_name__contains=search_content) &
            Q(owner_id=owner_id)
        )
        list_menu = list_menu.exclude(state="已删除")
    if sortType == 1:
        list_menu = list_menu.filter(state="已发布").order_by('-publish_time')
    elif sortType == 2:
        list_menu = list_menu.filter(state="已发布").order_by('publish_time')
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
    current_page = int(request.GET.get("currentPage"))
    page_current = list_menu[(current_page - 1) * num_one_page:current_page * num_one_page]
    total_page = int(list_menu.count() / num_one_page) + (list_menu.count() % num_one_page != 0)
    page_needed = ListSerializer(page_current, many=True)
    ret_data = {
        "totalPage": total_page,
        "list": page_needed.data
    }
    return JsonResponse(ret_data)


def register(request):
    data = json.loads(request.body)
    username = data.get("username")
    tmp = User.objects.filter(name=username)
    if tmp.exists():
        ret_data = {
            "message": "用户名已存在"
        }
        return JsonResponse(ret_data)
    user = User()
    user.name = data.get("username")
    user.password = data.get("password")
    user.save()
    ret_data = {
        "message": "注册成功"
    }
    return JsonResponse(ret_data)


def login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    tmp = User.objects.filter(name=username)
    if tmp.exists():
        tmp = User.objects.get(name=username)
        if tmp.password == password:
            ret_data = {
                "user_id": tmp.user_id
            }
            return JsonResponse(ret_data)
    ret_data = {
        "message": "用户名或密码错误"
    }
    return JsonResponse(ret_data)


def change_pass(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = User.objects.get(username=username)
    user.password = password
    user.save()
    ret_data = {
        "message": "密码修改成功"
    }
    return JsonResponse(ret_data)


def to_recycle(request):
    data = json.load(request)
    list_id = int(data.get("list_id"))
    list_changed = List.objects.get(list_id=list_id)
    list_changed.state = "已删除"
    list_changed.publish_time = None
    list_changed.save()
    ret_data = {
        "message": "问卷已删除，可在回收站中恢复或彻底删除"
    }
    return JsonResponse(ret_data)


def get_recycle_list(request):
    data = json.load(request)
    owner_id = int(data.get("usrID"))
    recycle_list = List.objects.filter(
        Q(owner_id=owner_id) &
        Q(state="已删除")
    )
    list_json = ListSerializer(recycle_list, many=True)
    ret_data = {
        "list": list_json.data
    }
    return JsonResponse(ret_data)
