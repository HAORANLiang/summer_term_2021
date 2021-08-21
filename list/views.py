import datetime
import json

from django.http import JsonResponse
from django.utils import timezone

from list.models import *
from question.models import *


def add_list(request):
    data = json.loads(request.body)
    new_list = List()
    new_list.state = "未发布"
    new_list.list_type = data.get("type")
    new_list.list_name = data.get("list_name")
    new_list.start_time = timezone.now()
    new_list.end_time = timezone.now()
    new_list.full_time = timezone.now()
    new_list.owner_id = data.get("owner_id")
    new_list.summary = data.get("summary")
    new_list.list_num = 0
    body = data.get("body")
    new_list.que_num = len(body)
    new_list.save()
    for que in body:
        que_qualify(new_list.list_id, que)
    ret_data = {
        "message": "submit success"
    }
    return JsonResponse(ret_data)


def que_qualify(list_id, que):
    new_que_build = Que_build()
    new_que_build.list_id = list_id
    new_que_build.que_no = que.get("no")
    new_que_build.que_type = que.get("type")
    case = {
        "single": add_single,
        "multi": add_multi,
        "pack": add_pack,
        "rate": add_rate
    }
    new_que_build.que_id = case.get(new_que_build.que_type)(que)
    new_que_build.save()


def add_single(single):
    new_single = Single()
    new_single.nec = single.get("nec")
    new_single.title = single.get("title")
    contents = single.get("content")
    new_single.content_num = len(contents)
    new_single.correct_id = single.get("correct_id")
    if new_single.content_num > 0:
        new_single.content_1 = contents[0]
    if new_single.content_num > 1:
        new_single.content_2 = contents[1]
    if new_single.content_num > 2:
        new_single.content_3 = contents[2]
    if new_single.content_num > 3:
        new_single.content_4 = contents[3]
    if new_single.content_num > 4:
        new_single.content_5 = contents[4]
    if new_single.content_num > 5:
        new_single.content_6 = contents[5]
    if new_single.content_num > 6:
        new_single.content_7 = contents[6]
    if new_single.content_num > 7:
        new_single.content_8 = contents[7]
    new_single.save()
    return new_single.single_id


def add_multi(multi):
    new_multi = Multi()
    new_multi.nec = multi.get("nec")
    new_multi.title = multi.get("title")
    contents = multi.get("content")
    new_multi.content_num = len(contents)
    if new_multi.content_num > 0:
        new_multi.content_1 = contents[0]
    if new_multi.content_num > 1:
        new_multi.content_2 = contents[1]
    if new_multi.content_num > 2:
        new_multi.content_3 = contents[2]
    if new_multi.content_num > 3:
        new_multi.content_4 = contents[3]
    if new_multi.content_num > 4:
        new_multi.content_5 = contents[4]
    if new_multi.content_num > 5:
        new_multi.content_6 = contents[5]
    if new_multi.content_num > 6:
        new_multi.content_7 = contents[6]
    if new_multi.content_num > 7:
        new_multi.content_8 = contents[7]
    new_multi.save()
    return new_multi.multi_id


def add_pack(pack):
    new_pack = Pack()
    new_pack.nec = pack.get("nec")
    new_pack.title = pack.get("title")
    new_pack.pack_num = get_blank_num(new_pack.title)
    new_pack.save()
    return new_pack.pack_id


def add_rate(rate):
    new_rate = Rate()
    new_rate.nec = rate.get("nec")
    new_rate.title = rate.get("title")
    new_rate.save()
    return new_rate.rate_id


def get_blank_num(string):
    pre = False
    num = 0
    for char in string:
        if char == '_':
            if not pre:
                pre = True
                num += 1
        else:
            pre = False
    return num


def recover(request):
    data = json.loads(request.body)
    owner_id = data.get("owner_id")
    list_id = data.get("list_id")
    list = List.objects.get(list_id=list_id)
    list.state = "未发布"
    list.save()
    ret_data = {
        "msg": "恢复成功"
    }
    return JsonResponse(ret_data)


def tot_delete(request):
    data = json.loads(request.body)
    owner_id = data.get("owner_id")
    list_id = data.get("list_id")
    list = List.objects.get(list_id=list_id)
    list.delete()
    ret_data = {
        "msg": "删除成功"
    }
    return JsonResponse(ret_data)
