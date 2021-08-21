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
    print(new_list.list_id)##
    for que in body:
        que_qualify(new_list.list_id, que)
    ret_data = {
        "message": "Success"
    }
    return JsonResponse(ret_data)


def que_type_switch(que_type, que):
    case = {
        "single": add_single(que)
    }
    return case.get(que_type, None)


def que_qualify(list_id, que):
    new_que_build = Que_build()
    new_que_build.list_id = list_id
    new_que_build.que_no = que.get("no")
    new_que_build.que_type = que.get("type")
    new_que_build.que_id = que_type_switch(new_que_build.que_type, que)
    new_que_build.save()


def add_single(single):
    new_single = Single()
    new_single.nec = single.get("nec")
    new_single.title = single.get("title")
    new_single.context_num = single.get("context_num")
    new_single.correct_id = single.get("correct_id")
    new_single.context_1 = single.get("context_1")
    print(new_single.context_1)##
    new_single.context_2 = single.get("context_2")
    new_single.context_3 = single.get("context_3")
    new_single.context_4 = single.get("context_4")
    new_single.context_5 = single.get("context_5")
    new_single.context_6 = single.get("context_6")
    new_single.context_7 = single.get("context_7")
    new_single.context_8 = single.get("context_8")
    new_single.save()
    return new_single.single_id
