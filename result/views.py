import datetime

from django.db.models import Max, Q
from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.http import JsonResponse,HttpResponse
import json
from result.models import *
from question.models import *
from list.models import *
import xlwt
from io import BytesIO


# Create your views here.
def save_result(request):
    data = json.loads(request.body)
    result = Result()
    result.list_id = data.get("id")
    List.objects.filter(
        Q(list_id=int(data.get("id"))) &
        Q(state="已发布") &
        Q(end_time__lt=datetime.datetime.now())
    ).update("未发布")
    if List.objects.get(list_id=int(data.get("id"))).state == "未发布":
        ret_data = {
            "message": "问卷已截止"
        }
        return JsonResponse(ret_data)
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
    results_num = Result.objects.filter(list_id=list_id).count()
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


def all_result_count(request):
    num = Result.objects.all().aggregate(Max('result_id'))
    return JsonResponse(num)


def to_excel(request):
    list_id = request.POST.get('list_id')
    list = List.objects.filter(list_id=list_id)
    results = Result.objects.filter(list_id=list_id)
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=' + str(list_id) + '.xls'
    """导出excel表"""

    # 创建工作簿
    ws = xlwt.Workbook(encoding='utf-8')
    # 添加第一页数据表
    w = ws.add_sheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
    # 写入表头
    builds = Que_build.objects.filter(list_id=list_id).order_by("que_no")
    i = 1
    for build in builds:
        name = ""
        question = ""
        if build.que_type == "single":
            question = Single.objects.get(single_id=build.que_id)
        if build.que_type == "multi":
            question = Multi.objects.get(multi_id=build.que_id)
        if build.que_type == "pack":
            question = Pack.objects.get(pack_id=build.que_id)
        if build.que_type == "rate":
            question = Rate.objects.get(rate_id=build.que_id)
        name = question.title
        w.write(0, i, name)
        i +=1
    # 写入数据
    results = Result.objects.filter(list_id=list_id)
    excel_row = 1
    for result in results:
        for j in (1, i):
            res_build = Result_build.objects.filter(result_id=result.result_id,que_no=j)
            name = ""
            content = ""
            if res_build.exists():
                res_build = Result_build.objects.get(result_id=result.result_id, que_no=j)
                if res_build.que_type == "single":
                    question = Single_ans.objects.get(single_id=res_build.que_id)
                    contents = [
                        question.content_1,
                        question.content_2,
                        question.content_3,
                        question.content_4,
                        question.content_5,
                        question.content_6,
                        question.content_7,
                        question.content_8,
                    ]
                    for i in range(8):
                        if contents[i] != 0:
                            content += str(contents[i]) + " "
                if res_build.que_type == "multi":
                    question = Multi_ans.objects.get(multi_id=res_build.que_id)
                    contents = [
                        question.content_1,
                        question.content_2,
                        question.content_3,
                        question.content_4,
                        question.content_5,
                        question.content_6,
                        question.content_7,
                        question.content_8,
                    ]
                    for i in range(8):
                        if contents[i] != 0:
                            content += str(contents[i]) + " "
                if res_build.que_type == "pack":
                    question = Pack_ans.objects.get(pack_id=res_build.que_id)
                    contents = [
                        question.content_1,
                        question.content_2,
                        question.content_3,
                        question.content_4,
                        question.content_5,
                    ]
                    for i in range(5):
                        if contents[i] != 0:
                            content += str(contents[i]) + " "
                if res_build.que_type == "rate":
                    question = Rate_ans.objects.get(rate_id=res_build.que_id)
                    content += str(question.ans)
                w.write(excel_row, j, content)

        excel_row += 1
    # 写出到IO
    output = BytesIO()
    ws.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response