import json
import datetime

from django.http import JsonResponse

from list.models import *
from question.models import *
from result.models import *


def add_list(request):
    data = json.loads(request.body)
    new_list = List()
    list_id = data.get("id")
    if not list_id == -1:
        new_list = List.objects.get(list_id=list_id)
        delete_association(list_id)
    else:
        new_list.state = "未发布"
    new_list.list_type = data.get("type")
    new_list.list_name = data.get("list_name")
    new_list.owner_id = data.get("owner_id")
    new_list.summary = data.get("summary")
    new_list.only_once = True
    new_list.need_login = True
    new_list.list_num = 0
    body = data.get("body")
    new_list.que_num = len(body)
    new_list.save()
    for que in body:
        que_qualify(new_list.list_id, que)
    ret_data = {
        "list_id": new_list.list_id
    }
    return JsonResponse(ret_data)


def delete_association(list_id):
    list_to_delete = Que_build.objects.filter(list_id=list_id)
    for build in list_to_delete:
        delete_type_qualify(build.que_type, build.que_id)
    Que_build.objects.filter(list_id=list_id).delete()
    Result_build.objects.filter(list_id=list_id).delete()


def delete_type_qualify(que_type, que_id):
    case = {
        "single": delete_single,
        "multi": delete_multi,
        "pack": delete_pack,
        "rate": delete_rate
    }
    case.get(que_type)(que_id)


def delete_single(single_id):
    Single.objects.filter(single_id=single_id).delete()


def delete_multi(multi_id):
    Multi.objects.filter(multi_id=multi_id).delete()


def delete_pack(pack_id):
    Pack.objects.filter(pack_id=pack_id).delete()


def delete_rate(rate_id):
    Rate.objects.filter(rate_id=rate_id).delete()


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
    new_single.description = single.get("description")
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
    new_multi.description = multi.get("description")
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
    new_pack.description = pack.get("description")
    new_pack.pack_num = get_blank_num(new_pack.title)
    new_pack.save()
    return new_pack.pack_id


def add_rate(rate):
    new_rate = Rate()
    new_rate.nec = rate.get("nec")
    new_rate.title = rate.get("title")
    new_rate.description = rate.get("description")
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
    delete_association(list_id)
    ret_data = {
        "msg": "删除成功"
    }
    return JsonResponse(ret_data)


def verity_quest(request):
    id = request.GET.get("id")
    list = List.objects.filter(list_id=id)
    if not list.exists():
        ret_data = {
            "msg": "问卷不存在"
        }
        return JsonResponse(ret_data)
    list = List.objects.get(list_id=id)
    if list.state != "已发布":
        ret_data = {
            "msg": "问卷未发布"
        }
        return JsonResponse(ret_data)
    user_id = request.headers.get("Authorization")
    if list.only_once == 1:
        tmp = Result.objects.filter(list_id=id, user_id=user_id)
        if tmp.exists():
            ret_data = {
                "msg": "此问卷不可重复填写"
            }
            return JsonResponse(ret_data)
    return quest(request)


def quest(request):
    id = request.GET.get("id")
    list = List.objects.filter(list_id=id)
    if not list.exists():
        ret_data = {
            "msg": "问卷不存在"
        }
        return JsonResponse(ret_data)
    list = List.objects.get(list_id=id)
    if list.state != "已发布":
        user_id = request.headers.get("Authorization")
        if int(user_id) != list.owner_id:
            ret_data = {
                "msg": "无权限访问"
            }
            return JsonResponse(ret_data)
    body = []
    index = Que_build.objects.filter(list_id=id).order_by('que_no')
    for tmp in index:
        type = tmp.que_type
        id = tmp.que_id
        if type == "single":
            question = Single.objects.get(single_id=id)
            content = []
            if question.content_1 != "":
                content.append(question.content_1)
            if question.content_2 != "":
                content.append(question.content_2)
            if question.content_3 != "":
                content.append(question.content_3)
            if question.content_4 != "":
                content.append(question.content_4)
            if question.content_5 != "":
                content.append(question.content_5)
            if question.content_6 != "":
                content.append(question.content_6)
            if question.content_7 != "":
                content.append(question.content_7)
            if question.content_8 != "":
                content.append(question.content_8)
            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,
                "content": content
            }
            body.append(group)
        if type == "multi":
            question = Multi.objects.get(multi_id=id)
            content = []
            if question.content_1 != "":
                content.append(question.content_1)
            if question.content_2 != "":
                content.append(question.content_2)
            if question.content_3 != "":
                content.append(question.content_3)
            if question.content_4 != "":
                content.append(question.content_4)
            if question.content_5 != "":
                content.append(question.content_5)
            if question.content_6 != "":
                content.append(question.content_6)
            if question.content_7 != "":
                content.append(question.content_7)
            if question.content_8 != "":
                content.append(question.content_8)
            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,
                "content": content
            }
            body.append(group)
        if type == "pack":
            question = Pack.objects.get(pack_id=id)

            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,

            }
            body.append(group)
        if type == "rate":
            question = Rate.objects.get(rate_id=id)

            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,

            }
            body.append(group)
    ret_data = {
        "list_name": list.list_name,
        "type": list.list_type,
        "owner_id": list.owner_id,
        "summary": list.summary,
        "body": body
    }
    return JsonResponse(ret_data)


def set_publish(request):
    list_id = int(request.GET.get("id"))
    publish = int(request.GET.get("publish"))
    if publish:
        state = "已发布"
        List.objects.filter(list_id=list_id).update(state=state, publish_time=datetime.datetime.now())
    else:
        state = "未发布"
        List.objects.filter(list_id=list_id).update(state=state, publish_time=None)
    ret_data = {
        "result": True
    }
    return JsonResponse(ret_data)


def get_publish(request):
    list_id = int(request.GET.get("id"))
    list_searched = List.objects.get(list_id=list_id)
    if list_searched.state == "已发布":
        state = 1
    elif list_searched.state == "未发布":
        state = 0
    else:
        state = 2
    if list_searched.start_time is None:
        start_time = ""
    else:
        start_time = json.dumps(list_searched.start_time.strftime('%Y-%m-%dT%H:%M:%S'))
    if list_searched.end_time is None:
        deadline = ""
    else:
        deadline = json.dumps(list_searched.end_time.strftime('%Y-%m-%dT%H:%M:%S'))
    ret_data = {
        "publish": state,
        "need_login": list_searched.need_login,
        "only_once": list_searched.only_once,
        "start_time": start_time,
        "deadline": deadline
    }
    return JsonResponse(ret_data)


def set_publish_info(request):
    list_id = int(request.GET.get("id"))
    need_login = int(request.GET.get("need_login"))
    only_once = int(request.GET.get("only_once"))
    list_changed = List.objects.get(list_id=list_id)
    list_changed.need_login = (need_login == 1)
    list_changed.only_once = (only_once == 1)
    str_start_time = request.GET.get("start_time")
    str_deadline = request.GET.get("deadline")
    if len(str_start_time) != 0:
        start_time = datetime.datetime.strptime(str_start_time, '%Y-%m-%dT%H:%M:%S')
    else:
        start_time = datetime.datetime.now()
    list_changed.start_time = start_time
    if len(str_deadline) != 0:
        deadline = datetime.datetime.strptime(str_deadline, '%Y-%m-%dT%H:%M:%S')
        list_changed.end_time = deadline
    else:
        list_changed.end_time = None
    # list_changed.full_time = deadline - start_time
    list_changed.save()
    ret_data = {
        "result": True
    }
    return JsonResponse(ret_data)
