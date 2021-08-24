from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.http import JsonResponse
import json
from result.models import *
from question.models import *
from list.models import *


# Create your views here.
def save_result(request):
    data = json.loads(request.body)
    result = Result()
    result.list_id = data.get("id")
    if data.get("user_id") != "null":
        result.user_id = data.get("user_id")
    result.save()
    answers = data.get("answer")
    list = List.objects.get(list_id=result.list_id)
    list.list_num = list.list_num+1
    list.save()
    for i in range(len(answers)):
        answer = answers[i]
        finish = answer.get("finish")
        que_build = Que_build.objects.get(list_id=result.list_id, que_no=i+1)
        type = que_build.que_type
        if finish == 1:
            if type == "single":
                single_ans = Single_ans()

                single_ans.ans = answer.get("content")[0]
                single_ans.save()
                result_build = Result_build()
                result_build.list_id = result.list_id
                result_build.result_id = result.result_id
                result_build.que_no = i+1
                result_build.que_type = type
                result_build.que_id = single_ans.single_id
                result_build.save()
            if type == "multi":
                multi_ans = Multi_ans()

                ans = answer.get("content")
                multi_ans.num =len(ans)
                if multi_ans.num>7:
                    multi_ans.ans8 = ans[7]
                if multi_ans.num>6:
                    multi_ans.ans7 = ans[6]
                if multi_ans.num>5:
                    multi_ans.ans6 = ans[5]
                if multi_ans.num>4:
                    multi_ans.ans5 = ans[4]
                if multi_ans.num>3:
                    multi_ans.ans4 = ans[3]
                if multi_ans.num>2:
                    multi_ans.ans3 = ans[2]
                if multi_ans.num>1:
                    multi_ans.ans2 = ans[1]
                if multi_ans.num>0:
                    multi_ans.ans1 = ans[0]

                multi_ans.save()
                result_build = Result_build()
                result_build.list_id = result.list_id
                result_build.result_id = result.result_id
                result_build.que_no = i+1
                result_build.que_type = type
                result_build.que_id = multi_ans.multi_id
                result_build.save()
            if type == "pack":
                pack_ans = Pack_ans()

                ans = answer.get("content")
                pack_ans.num = len(ans)

                if pack_ans.num > 4:
                    pack_ans.ans5 = ans[4]
                if pack_ans.num > 3:
                    pack_ans.ans4 = ans[3]
                if pack_ans.num > 2:
                    pack_ans.ans3 = ans[2]
                if pack_ans.num > 1:
                    pack_ans.ans2 = ans[1]
                if pack_ans.num > 0:
                    pack_ans.ans1 = ans[0]

                pack_ans.save()
                result_build = Result_build()
                result_build.list_id = result.list_id
                result_build.result_id = result.result_id
                result_build.que_no = i+1
                result_build.que_type = type
                result_build.que_id = pack_ans.pack_id
                result_build.save()
            if type == "rate":
                rate_ans = Rate_ans()

                rate_ans.ans = answer.get("content")
                rate_ans.save()
                result_build = Result_build()
                result_build.list_id = result.list_id
                result_build.result_id = result.result_id
                result_build.que_no = i+1
                result_build.que_type = type
                result_build.que_id = rate_ans.rate_id
                result_build.save()
    ret_data = {
        'message': "submit success"
    }
    return JsonResponse(ret_data, safe=False)


def statistic(request):
    list_id = request.GET.get("id")
    list = List.objects.get(list_id=list_id)
    results = Result.objects.filter(list_id=list_id)
    results_num = Result_build.objects.filter(list_id=list_id).count()
    que = []
    builds = Que_build.objects.filter(list_id=list_id).order_by('que_no')
    for build in builds:
        que_id = build.que_id
        type = build.que_type
        res_builds = Result_build.objects.filter(list_id=list_id, que_no=build.que_no)
        num = Result_build.objects.filter(list_id=list_id, que_no=build.que_no).count()
        if type == "single":
            question = Single.objects.get(single_id=que_id)
            rate = {}
            x=[0,0,0,0,0,0,0,0]
            for res_build in res_builds:
                result_id = res_build.que_id
                result = Single_ans.objects.get(single_id=result_id)
                for i in range(8):
                    if result.ans == i:
                        x[i] += 1

            if question.content_1 != "":
                tmp = {question.content_1: 0 if (num==0) else int(float(x[0])/num*100)}
                rate.update(tmp)
            if question.content_2 != "":
                tmp = {question.content_2: 0 if (num==0) else int(float(x[1])/num*100)}
                rate.update(tmp)
            if question.content_3 != "":
                tmp = {question.content_3: 0 if (num==0) else int(float(x[2])/num*100)}
                rate.update(tmp)
            if question.content_4 != "":
                tmp = {question.content_4: 0 if (num==0) else int(float(x[3])/num*100)}
                rate.update(tmp)
            if question.content_5 != "":
                tmp = {question.content_5: 0 if (num==0) else int(float(x[4])/num*100)}
                rate.update(tmp)
            if question.content_6 != "":
                tmp = {question.content_6: 0 if (num==0) else int(float(x[5])/num*100)}
                rate.update(tmp)
            if question.content_7 != "":
                tmp = {question.content_7: 0 if (num==0) else int(float(x[6])/num*100)}
                rate.update(tmp)
            if question.content_8 != "":
                tmp = {question.content_8: 0 if (num==0) else int(float(x[7])/num*100)}
                rate.update(tmp)
            tmp_que = {
                'no': build.que_no,
                'title': question.title,
                'description': question.description,
                'type': type,
                'all': num,
                'all_rate': 0 if (num==0) else int(float(num)/results_num*100),
                'rate': rate
            }
            que.append(tmp_que)
        if type == "multi":
            question = Multi.objects.get(multi_id=que_id)
            rate = {}
            x = [0, 0, 0, 0, 0, 0, 0, 0]
            for res_build in res_builds:
                result_id = res_build.que_id
                result = Multi_ans.objects.get(multi_id=result_id)
                for i in range(8):
                    if result.ans1 == i:
                        x[i] += 1
                for i in range(8):
                    if result.ans2 == i:
                        x[i] += 1
                for i in range(8):
                    if result.ans3 == i:
                        x[i] += 1
                for i in range(8):
                    if result.ans4 == i:
                        x[i] += 1
                for i in range(8):
                    if result.ans5 == i:
                        x[i] += 1
                for i in range(8):
                    if result.ans6 == i:
                        x[i] += 1
                for i in range(8):
                    if result.ans7 == i:
                        x[i] += 1
                for i in range(8):
                    if result.ans8 == i:
                        x[i] += 1
            if question.content_1 != "":
                tmp = {question.content_1: 0 if (num == 0) else int(float(x[0]) / num * 100)}
                rate.update(tmp)
            if question.content_2 != "":
                tmp = {question.content_2: 0 if (num == 0) else int(float(x[1]) / num * 100)}
                rate.update(tmp)
            if question.content_3 != "":
                tmp = {question.content_3: 0 if (num == 0) else int(float(x[2]) / num * 100)}
                rate.update(tmp)
            if question.content_4 != "":
                tmp = {question.content_4: 0 if (num == 0) else int(float(x[3]) / num * 100)}
                rate.update(tmp)
            if question.content_5 != "":
                tmp = {question.content_5: 0 if (num == 0) else int(float(x[4]) / num * 100)}
                rate.update(tmp)
            if question.content_6 != "":
                tmp = {question.content_6: 0 if (num == 0) else int(float(x[5]) / num * 100)}
                rate.update(tmp)
            if question.content_7 != "":
                tmp = {question.content_7: 0 if (num == 0) else int(float(x[6]) / num * 100)}
                rate.update(tmp)
            if question.content_8 != "":
                tmp = {question.content_8: 0 if (num == 0) else int(float(x[7]) / num * 100)}
                rate.update(tmp)
            tmp_que = {
                'no': build.que_no,
                'title': question.title,
                'description': question.description,
                'type': type,
                'all': num,
                'all_rate': 0 if (num == 0) else int(float(num) / results_num * 100),
                'rate': rate
            }
            que.append(tmp_que)
        if type == "rate":
            question = Rate.objects.get(rate_id=que_id)
            rate = {}
            x=[0,0,0,0,0,0,0,0,0,0,0]
            for res_build in res_builds:
                result_id = res_build.que_id
                result = Rate_ans.objects.get(rate_id=result_id)
                for i in range(11):
                    if result.ans == i:
                        x[i] += 1
            for i in range(10):
                tmp = {str(i+1): 0 if (num==0) else int(float(x[i+1])/num*100)}
                rate.update(tmp)
            tmp_que = {
                'no': build.que_no,
                'title': question.title,
                'description': question.description,
                'type': type,
                'all': num,
                'all_rate': 0 if (num==0) else int(float(num)/results_num*100),
                'rate': rate
            }
            que.append(tmp_que)
        if type == "pack":
            question = Pack.objects.get(pack_id=que_id)

            tmp_que = {
                'no': build.que_no,
                'title': question.title,
                'description': question.description,
                'type': type,
                'all': num,
                'all_rate': 0 if (num==0) else int(float(num)/results_num*100),

            }
            que.append(tmp_que)
    ret_data = {
        "name": list.list_name,
        "id": list.list_id,
        "que": que
    }
    return JsonResponse(ret_data)