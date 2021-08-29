import json
import datetime

from django.http import JsonResponse
from random import Random
from list.models import *
from question.models import *
from result.models import *
from result.views import *


def add_list(request):
    data = json.loads(request.body)
    new_list = List()
    list_id = data.get("id")
    if not list_id == -1:
        new_list = List.objects.get(list_id=list_id)
        delete_association(list_id)
        Sequence.objects.filter(list_id=list_id).delete()
    else:
        new_list.state = "未发布"
        new_list.only_once = False
        new_list.need_login = False
    new_list.list_type = data.get("list_type")
    new_list.list_name = data.get("list_name")
    new_list.owner_id = data.get("owner_id")
    new_list.summary = data.get("summary")
    new_list.displayNumber = data.get("displayNumber")
    new_list.list_num = 0
    body = data.get("body")
    new_list.que_num = len(body)
    new_list.code = generate_code()
    new_list.save()
    for que in body:
        que_qualify(new_list.list_id, que, new_list.list_type)
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
    Result.objects.filter(list_id=list_id).delete()


def delete_type_qualify(que_type, que_id):
    case = {
        "single": delete_single,
        "multi": delete_multi,
        "pack": delete_pack,
        "rate": delete_rate,
        "positionp": delete_pack
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


def que_qualify(list_id, que, list_type):
    new_que_build = Que_build()
    new_que_build.list_id = list_id
    new_que_build.que_no = que.get("no")
    new_que_build.que_type = que.get("type")
    case = {
        "single": add_single,
        "multi": add_multi,
        "pack": add_pack,
        "rate": add_rate,
        "positionp": add_pack
    }
    new_que_build.que_id = case.get(new_que_build.que_type)(list_id, que, list_type)
    new_que_build.save()


def add_single(list_id, single, list_type):
    new_single = Single()
    new_single.nec = single.get("nec")
    new_single.title = single.get("title")
    new_single.description = single.get("description")
    contents = single.get("content")
    new_single.content_num = len(contents)
    new_single.correct_id = single.get("correct_id")
    new_single.score = single.get("score")
    new_single.is_exam = single.get("isExam")
    new_single.is_apply = single.get("isApply")
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
    right_answer = single.get("right_answer")
    add_right_choice(new_single, right_answer)
    leave = single.get("leave")
    add_leave(new_single, leave)
    new_single.save()
    pre = single.get("pre")
    if pre != {}:
        add_pre(new_single, pre, new_single.single_id, list_id)
    new_single.save()
    return new_single.single_id


def add_pre(que, pre, que_id, list_id):
    for each_key in pre:
        # print(int(each_key))
        new_sequence = Sequence()
        new_sequence.list_id = list_id
        new_sequence.que_id = que_id
        new_sequence.pre_id = int(each_key)
        content = pre[each_key]
        for each_content in content:
            if each_content == 0:
                new_sequence.pre_content_1 = True
            if each_content == 1:
                new_sequence.pre_content_2 = True
            if each_content == 2:
                new_sequence.pre_content_3 = True
            if each_content == 3:
                new_sequence.pre_content_4 = True
            if each_content == 4:
                new_sequence.pre_content_5 = True
            if each_content == 5:
                new_sequence.pre_content_6 = True
            if each_content == 6:
                new_sequence.pre_content_7 = True
            if each_content == 7:
                new_sequence.pre_content_8 = True
        new_sequence.save()


def add_right_choice(que, right_answer):
    for each_ans in right_answer:
        if each_ans == 0:
            que.content_1_isTrue = True
        elif each_ans == 1:
            que.content_2_isTrue = True
        elif each_ans == 2:
            que.content_3_isTrue = True
        elif each_ans == 3:
            que.content_4_isTrue = True
        elif each_ans == 4:
            que.content_5_isTrue = True
        elif each_ans == 5:
            que.content_6_isTrue = True
        elif each_ans == 6:
            que.content_7_isTrue = True
        elif each_ans == 7:
            que.content_8_isTrue = True


def add_leave(que, leave):
    if leave is None:
        return
    num = len(leave)
    if num > 0:
        que.content_1_leave = int(leave[0])
    if num > 1:
        que.content_2_leave = int(leave[1])
    if num > 2:
        que.content_3_leave = int(leave[2])
    if num > 3:
        que.content_4_leave = int(leave[3])
    if num > 4:
        que.content_5_leave = int(leave[4])
    if num > 5:
        que.content_6_leave = int(leave[5])
    if num > 6:
        que.content_7_leave = int(leave[6])
    if num > 7:
        que.content_8_leave = int(leave[7])


def add_multi(list_id, multi, list_type):
    new_multi = Multi()
    new_multi.nec = multi.get("nec")
    new_multi.title = multi.get("title")
    new_multi.description = multi.get("description")
    new_multi.score = multi.get("score")
    contents = multi.get("content")
    new_multi.is_exam = multi.get("isExam")
    new_multi.is_apply = multi.get("isApply")
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
    right_answer = multi.get("right_answer")
    add_right_choice(new_multi, right_answer)
    leave = multi.get("leave")
    add_leave(new_multi, leave)
    new_multi.save()
    pre = multi.get("pre")
    if pre != {}:
        add_pre(new_multi, pre, new_multi.multi_id, list_id)
    new_multi.save()
    return new_multi.multi_id


def add_pack(list_id, pack, list_type):
    new_pack = Pack()
    new_pack.nec = pack.get("nec")
    new_pack.title = pack.get("title")
    new_pack.description = pack.get("description")
    new_pack.score = pack.get("score")
    new_pack.pack_num = get_blank_num(new_pack.title)
    right_answer = pack.get("right_answer")
    new_pack.is_exam = pack.get("isExam")
    new_pack.is_apply = pack.get("isApply")
    num = len(right_answer)
    if num > 0:
        new_pack.pack_ans_1 = right_answer[0]
    if num > 1:
        new_pack.pack_ans_2 = right_answer[1]
    if num > 2:
        new_pack.pack_ans_3 = right_answer[2]
    if num > 3:
        new_pack.pack_ans_4 = right_answer[3]
    if num > 4:
        new_pack.pack_ans_5 = right_answer[4]
    new_pack.save()
    pre = pack.get("pre")
    if pre != {}:
        add_pre(new_pack, pre, new_pack.pack_id, list_id)
    new_pack.save()
    return new_pack.pack_id


def add_rate(list_id, rate, list_type):
    new_rate = Rate()
    new_rate.nec = rate.get("nec")
    new_rate.title = rate.get("title")
    new_rate.description = rate.get("description")
    new_rate.is_exam = rate.get("isExam")
    new_rate.is_apply = rate.get("isApply")
    new_rate.save()
    pre = rate.get("pre")
    if pre != {}:
        add_pre(new_rate, pre, new_rate.rate_id, list_id)
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
    if num != 0:
        return num
    else:
        return 1


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
            "isPublished": 0,
            "needLogin": 0
        }
        return JsonResponse(ret_data)
    user_id = request.headers.get("Authorization")
    if list.need_login is True:
        if user_id == '0':
            ret_data = {
                "isPublished": 1,
                "needLogin": 1
            }
            return JsonResponse(ret_data)
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
            leave = []
            if list.list_type == "apply":
                if question.content_1_leave is not None:
                    leave.append(question.content_1_leave)
                if question.content_2_leave is not None:
                    leave.append(question.content_2_leave)
                if question.content_3_leave is not None:
                    leave.append(question.content_3_leave)
                if question.content_4_leave is not None:
                    leave.append(question.content_4_leave)
                if question.content_5_leave is not None:
                    leave.append(question.content_5_leave)
                if question.content_6_leave is not None:
                    leave.append(question.content_6_leave)
                if question.content_7_leave is not None:
                    leave.append(question.content_7_leave)
                if question.content_8_leave is not None:
                    leave.append(question.content_8_leave)
            right_answer = []
            if list.list_type == "exam":
                if question.content_1_isTrue:
                    right_answer.append(0)
                if question.content_2_isTrue:
                    right_answer.append(1)
                if question.content_3_isTrue:
                    right_answer.append(2)
                if question.content_4_isTrue:
                    right_answer.append(3)
                if question.content_5_isTrue:
                    right_answer.append(4)
                if question.content_6_isTrue:
                    right_answer.append(5)
                if question.content_7_isTrue:
                    right_answer.append(6)
                if question.content_8_isTrue:
                    right_answer.append(7)
            pre = {}
            the_sequence = Sequence.objects.filter(que_id=question.single_id).order_by('pre_id')
            if the_sequence is not None:
                for each_sequence in the_sequence:
                    content = []
                    if each_sequence.pre_content_1:
                        content.append(0)
                    if each_sequence.pre_content_2:
                        content.append(1)
                    if each_sequence.pre_content_3:
                        content.append(2)
                    if each_sequence.pre_content_4:
                        content.append(3)
                    if each_sequence.pre_content_5:
                        content.append(4)
                    if each_sequence.pre_content_6:
                        content.append(5)
                    if each_sequence.pre_content_7:
                        content.append(6)
                    if each_sequence.pre_content_8:
                        content.append(7)
                    pre[each_sequence.pre_id] = content
            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,
                "content": content,
                "leave": leave,
                "score": question.score,
                "right_answer": right_answer,
                "pre": pre,
                "isExam": question.is_exam,
                "isApply": question.is_apply
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
            leave = []
            if list.list_type == "apply":
                if question.content_1_leave is not None:
                    leave.append(question.content_1_leave)
                if question.content_2_leave is not None:
                    leave.append(question.content_2_leave)
                if question.content_3_leave is not None:
                    leave.append(question.content_3_leave)
                if question.content_4_leave is not None:
                    leave.append(question.content_4_leave)
                if question.content_5_leave is not None:
                    leave.append(question.content_5_leave)
                if question.content_6_leave is not None:
                    leave.append(question.content_6_leave)
                if question.content_7_leave is not None:
                    leave.append(question.content_7_leave)
                if question.content_8_leave is not None:
                    leave.append(question.content_8_leave)
            right_answer = []
            if list.list_type == "exam":
                if question.content_1_isTrue:
                    right_answer.append(0)
                if question.content_2_isTrue:
                    right_answer.append(1)
                if question.content_3_isTrue:
                    right_answer.append(2)
                if question.content_4_isTrue:
                    right_answer.append(3)
                if question.content_5_isTrue:
                    right_answer.append(4)
                if question.content_6_isTrue:
                    right_answer.append(5)
                if question.content_7_isTrue:
                    right_answer.append(6)
                if question.content_8_isTrue:
                    right_answer.append(7)
            pre = {}
            the_sequence = Sequence.objects.filter(que_id=question.multi_id).order_by('pre_id')
            if the_sequence is not None:
                for each_sequence in the_sequence:
                    content = []
                    if each_sequence.pre_content_1:
                        content.append(0)
                    if each_sequence.pre_content_2:
                        content.append(1)
                    if each_sequence.pre_content_3:
                        content.append(2)
                    if each_sequence.pre_content_4:
                        content.append(3)
                    if each_sequence.pre_content_5:
                        content.append(4)
                    if each_sequence.pre_content_6:
                        content.append(5)
                    if each_sequence.pre_content_7:
                        content.append(6)
                    if each_sequence.pre_content_8:
                        content.append(7)
                    pre[each_sequence.pre_id] = content
            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,
                "content": content,
                "leave": leave,
                "score": question.score,
                "right_answer": right_answer,
                "pre": pre,
                "isExam": question.is_exam,
                "isApply": question.is_apply
            }
            body.append(group)
        if type == "pack" or type == "positionp":
            question = Pack.objects.get(pack_id=id)
            right_answer = []
            if list.list_type == "exam":
                if question.pack_ans_1 is not None:
                    # print(question.pack_ans_1)
                    right_answer.append(question.pack_ans_1)
                if question.pack_ans_2 is not None:
                    # print(question.pack_ans_2)
                    right_answer.append(question.pack_ans_2)
                if question.pack_ans_3 is not None:
                    # print(question.pack_ans_3)
                    right_answer.append(question.pack_ans_3)
                if question.pack_ans_4 is not None:
                    # print(question.pack_ans_4)
                    right_answer.append(question.pack_ans_4)
                if question.pack_ans_5 is not None:
                    # print(question.pack_ans_5)
                    right_answer.append(question.pack_ans_5)
            pre = {}
            the_sequence = Sequence.objects.filter(que_id=question.pack_id).order_by('pre_id')
            if the_sequence is not None:
                for each_sequence in the_sequence:
                    content = []
                    if each_sequence.pre_content_1:
                        content.append(0)
                    if each_sequence.pre_content_2:
                        content.append(1)
                    if each_sequence.pre_content_3:
                        content.append(2)
                    if each_sequence.pre_content_4:
                        content.append(3)
                    if each_sequence.pre_content_5:
                        content.append(4)
                    if each_sequence.pre_content_6:
                        content.append(5)
                    if each_sequence.pre_content_7:
                        content.append(6)
                    if each_sequence.pre_content_8:
                        content.append(7)
                    pre[each_sequence.pre_id] = content
            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,
                "score": question.score,
                "right_answer": right_answer,
                "pre": pre,
                "isExam": question.is_exam,
                "isApply": question.is_apply
            }
            body.append(group)
        if type == "rate":
            question = Rate.objects.get(rate_id=id)
            pre = {}
            the_sequence = Sequence.objects.filter(que_id=question.rate_id).order_by('pre_id')
            if the_sequence is not None:
                for each_sequence in the_sequence:
                    content = []
                    if each_sequence.pre_content_1:
                        content.append(0)
                    if each_sequence.pre_content_2:
                        content.append(1)
                    if each_sequence.pre_content_3:
                        content.append(2)
                    if each_sequence.pre_content_4:
                        content.append(3)
                    if each_sequence.pre_content_5:
                        content.append(4)
                    if each_sequence.pre_content_6:
                        content.append(5)
                    if each_sequence.pre_content_7:
                        content.append(6)
                    if each_sequence.pre_content_8:
                        content.append(7)
                    pre[each_sequence.pre_id] = content
            group = {
                "no": tmp.que_no,
                "type": tmp.que_type,
                "title": question.title,
                "description": question.description,
                "nec": question.nec,
                "pre": pre,
                "isExam": question.is_exam,
                "isApply": question.is_apply
            }
            body.append(group)
    if list.end_time is None:
        deadline = ""
    else:
        deadline = json.dumps(list.end_time.strftime('%Y-%m-%dT%H:%M:%S'))
    ret_data = {
        "list_name": list.list_name,
        "list_id": list.list_id,
        "type": list.list_type,
        "owner_id": list.owner_id,
        "summary": list.summary,
        "deadline": deadline,
        "displayNumber": list.displayNumber,
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
    """
    if list_searched.start_time is None:
        start_time = ""
    else:
        start_time = json.dumps(list_searched.start_time.strftime('%Y-%m-%dT%H:%M:%S'))
    """
    if list_searched.end_time is None:
        deadline = ""
    else:
        deadline = json.dumps(list_searched.end_time.strftime('%Y-%m-%dT%H:%M:%S'))
    if list_searched.show_result:
        is_show_result = 1
    else:
        is_show_result = 0
    ret_data = {
        "publish": state,
        "need_login": list_searched.need_login,
        "only_once": list_searched.only_once,
        # "start_time": start_time,
        "deadline": deadline,
        "showResult": is_show_result
    }
    return JsonResponse(ret_data)


def set_publish_info(request):
    list_id = int(request.GET.get("id"))
    need_login = int(request.GET.get("need_login"))
    only_once = int(request.GET.get("only_once"))
    list_changed = List.objects.get(list_id=list_id)
    if need_login == 1:
        list_changed.need_login = True
    else:
        list_changed.need_login = False
    if only_once == 1:
        list_changed.only_once = True
    else:
        list_changed.only_once = False
    list_changed.start_time = datetime.datetime.now()
    str_deadline = request.GET.get("deadline")
    if len(str_deadline) != 0:
        deadline = datetime.datetime.strptime(str_deadline, '"%Y-%m-%dT%H:%M:%S"')
        list_changed.end_time = deadline
    else:
        list_changed.end_time = None
    is_show_result = int(request.GET.get("showResult"))
    if is_show_result == 1:
        list_changed.show_result = True
    else:
        list_changed.show_result = False
    """
    str_start_time = request.GET.get("start_time")
    if len(str_start_time) != 0:
        start_time = datetime.datetime.strptime(str_start_time, '%Y-%m-%dT%H:%M:%S')
    else:
        
    list_changed.start_time = start_time
    if list_changed.end_time is not None:
        if list_changed.end_time - list_changed.start_time < datetime.timedelta(0):
            ret_data = {
                "message": "time set problem"
            }
            return JsonResponse(ret_data)
    """
    # list_changed.full_time = deadline - start_time
    list_changed.save()
    ret_data = {
        "result": True
    }
    return JsonResponse(ret_data)


def generate_code(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def new_code(request):
    data = json.loads(request.body)
    list_id = data.get("list_id")
    code = generate_code()
    list = List.objects.get(list_id=list_id)
    list.code = code
    list.save()
    ret_data = {
        "new_code": code
    }
    return JsonResponse(ret_data)


def get_code(request):
    data = json.loads(request.body)
    list_id = data.get("list_id")
    list = List.objects.get(list_id=list_id)
    if list.code == "":
        list.code = generate_code()
        list.save()
    code = list.code
    ret_data = {
        "old_code": code
    }
    return JsonResponse(ret_data)


def verify_code(request):
    code = request.GET.get("code")
    list = List.objects.filter(code=code)
    if not list.exists():
        ret_data = {
            "list_id": ""
        }
        return JsonResponse(ret_data)
    list = List.objects.get(code=code)
    list_id = list.list_id
    ret_data = {
        "list_id": list_id
    }
    return JsonResponse(ret_data)


def code_quest(request):
    code = request.GET.get("code")
    list = List.objects.filter(code=code)
    if not list.exists():
        ret_data = {
            "isPublished": 0,
            "needLogin": 0,
            "available": 0
        }
        return JsonResponse(ret_data)
    list = List.objects.get(code=code)
    if list.state != "已发布":
        ret_data = {
            "isPublished": 0,
            "needLogin": 0,
            "available": 1
        }
        return JsonResponse(ret_data)
    user_id = request.headers.get("Authorization")
    if list.need_login is True:
        if user_id == '0':
            ret_data = {
                "isPublished": 1,
                "needLogin": 1,
                "available": 1
            }
            return JsonResponse(ret_data)
        if list.only_once == 1:
            tmp = Result.objects.filter(list_id=list.list_id, user_id=user_id)
            if tmp.exists():
                ret_data = {
                    "msg": "此问卷不可重复填写"
                }
                return JsonResponse(ret_data)
    data = request.GET.copy()
    # 修改参数值
    tmp = {"id": list.list_id}
    data.update(tmp)
    if data:
        request.GET = data
    return quest(request)


def new_quest(request):
    code = request.GET.get("code")
    list = List.objects.filter(code=code)
    if not list.exists():
        ret_data = {
            "isPublished": 0,
            "needLogin": 0,
            "available": 0
        }
        return JsonResponse(ret_data)
    list = List.objects.get(code=code)
    if list.state != "已发布":
        ret_data = {
            "isPublished": 0,
            "needLogin": 0,
            "available": 1
        }
        return JsonResponse(ret_data)
    user_id = request.headers.get("Authorization")
    if list.need_login is True:
        if user_id == '0':
            ret_data = {
                "isPublished": 1,
                "needLogin": 1,
                "available": 1
            }
            return JsonResponse(ret_data)

    data = request.GET.copy()
    # 修改参数值
    tmp = {"id": list.list_id}
    data.update(tmp)
    if data:
        request.GET = data
    return quest(request)