import datetime
import json

from django.http import JsonResponse
from list.models import *
from question.models import *


def add_list(request):
    data = json.loads(request.body)
    new_list = List()
    new_list.state = data.get("state")
    new_list.list_type = data.get("list_type")
    new_list.list_name = data.get("list_name")
    # new_list.full_time = data.get("full_time")
    # new_list.start_time = data.get("start_time")
    # new_list.end_time = data.get("end_time")
    # new_list.last_edit_time = data.get("last_edit_time")
    new_list.full_time = datetime.datetime.now()##test
    new_list.start_time = datetime.datetime.now()##test
    new_list.end_time = datetime.datetime.now()##test
    new_list.last_edit_time = datetime.datetime.now()##test
    new_list.owner_id = data.get("owner_id")
    new_list.que_num = data.get("que_num")
    new_list.summary = data.get("summary")
    new_list.list_num = 0
    body = data.get("body")
    new_list.save()
    for que in body:
        que_qualify(new_list.list_id, que)
    ret_data = {
        "message": "Success"
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
    new_single.content_num = single.get("content_num")
    new_single.correct_id = single.get("correct_id")
    contents = single.get("content")
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
    new_multi.content_num = multi.get("content_num")
    contents = multi.get("content")
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
    new_pack.pack_num = pack.get("pack_num")
    new_pack.save()
    return new_pack.pack_id


def add_rate(rate):
    new_rate = Rate()
    new_rate.nec = rate.get("nec")
    new_rate.title = rate.get("title")
    new_rate.save()
    return new_rate.rate_id
