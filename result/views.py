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
from owner.models import *
import xlwt
from io import BytesIO


# Create your views here.
def save_result(request):
    data = json.loads(request.body)
    result = Result()
    result.submit_time = datetime.datetime.now()
    result.list_id = data.get("id")
    result.score = 0
    list_id = int(data.get("id"))
    the_list = List.objects.get(list_id=list_id)
    if the_list.state == "已发布" and the_list.end_time is not None:
            if the_list.end_time - datetime.datetime.now() < datetime.timedelta(0):
                the_list.state = "未发布"
                the_list.save()
    """
    List.objects.filter(
        Q(list_id=int(data.get("id"))) &
        Q(state="已发布") &
        Q(end_time__lt=datetime.datetime.now())
    ).update("未发布")
    """
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
        'message': "submit success",
        'result_id': result.result_id
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
    #list_id = request.POST.get('list_id')
    data = json.loads(request.body)
    list_id = data.get("list_id")
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
    w.write(0, 0, "用户名")
    w.write(0, 1,  "创建时间")
    i = 2
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
        user = User.objects.filter(user_id=result.user_id)
        if user.exists():
            user = User.objects.get(user_id=result.user_id)
            w.write(excel_row, 0, user.name)
        else:
            w.write(excel_row, 0, "null")
        w.write(excel_row, 1, result.submit_time)
        for j in range(1, i+1):
            res_build = Result_build.objects.filter(result_id=result.result_id,que_no=j)
            name = ""
            content = ""
            if res_build.exists():
                res_build = Result_build.objects.get(result_id=result.result_id, que_no=j)
                if res_build.que_type == "single":
                    question = Single_ans.objects.get(single_id=res_build.que_id)
                    content += str(question.ans) + " "
                if res_build.que_type == "multi":
                    question = Multi_ans.objects.get(multi_id=res_build.que_id)
                    contents = [
                        question.ans1,
                        question.ans2,
                        question.ans3,
                        question.ans4,
                        question.ans5,
                        question.ans6,
                        question.ans7,
                        question.ans8,
                    ]
                    for i in range(8):
                        if str(contents[i]) != "None":
                            content += str(contents[i]) + " "
                if res_build.que_type == "pack":
                    question = Pack_ans.objects.get(pack_id=res_build.que_id)
                    contents = [
                        question.ans1,
                        question.ans2,
                        question.ans3,
                        question.ans4,
                        question.ans5,
                    ]
                    for i in range(5):
                        if str(contents[i]) != "None":
                            content += str(contents[i]) + " "
                if res_build.que_type == "rate":
                    question = Rate_ans.objects.get(rate_id=res_build.que_id)
                    content += str(question.ans)
                w.write(excel_row, j+1, content)
        excel_row += 1
    # 写出到IO
    output = BytesIO()
    ws.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def check_ans(request):
    result_id = request.GET.get("result_id")
    result = Result.objects.get(result_id=result_id)
    list_id = result.list_id
    list = List.objects.get(list_id=list_id)
    score = 0
    rank = 0
    rightNum = 0
    tot_score = 0
    question_num = Que_build.objects.filter(list_id=list_id).count()
    builds = Que_build.objects.filter(list_id=list_id)
    for build in builds:
        x = 0
        if build.que_type == "single":
            question = Single.objects.get(single_id=build.que_id)
            if question.score is not None:
                x=question.score
        if build.que_type == "nulti":
            question = Multi.objects.get(multi_id=build.que_id)
            if question.score is not None:
                x = question.score
        if build.que_type == "pack":
            question = Pack.objects.get(pack_id=build.que_id)
            if question.score is not None:
                x = question.score
        tot_score += x
    answer = []
    res_builds = Result_build.objects.filter(result_id=result_id).order_by("que_no")
    for res_build in res_builds:
        build = Que_build.objects.get(list_id=res_build.list_id,que_no=res_build.que_no)
        if res_build.que_type == "single":
            res = Single_ans.objects.get(single_id=res_build.que_id)
            question = Single.objects.get(single_id=build.que_id)
            tmp = {
                "content": [res.ans]
            }
            answer.append(tmp)
            ans = []
            if question.content_1_isTrue == 1:
                ans.append(0)
            if question.content_2_isTrue == 1:
                ans.append(1)
            if question.content_3_isTrue == 1:
                ans.append(2)
            if question.content_4_isTrue == 1:
                ans.append(3)
            if question.content_5_isTrue == 1:
                ans.append(4)
            if question.content_6_isTrue == 1:
                ans.append(5)
            if question.content_7_isTrue == 1:
                ans.append(6)
            if question.content_8_isTrue == 1:
                ans.append(7)
            if len(ans)>0:
                if ans[0] == int(res.ans):
                    score += question.score
                    rightNum += 1
        if res_build.que_type == "multi":
            res = Multi_ans.objects.get(multi_id=res_build.que_id)
            question = Multi.objects.get(multi_id=build.que_id)
            content = []
            if res.ans1 is not None:
                content.append(int(res.ans1))
            if res.ans2 is not None:
                content.append(int(res.ans2))
            if res.ans3 is not None:
                content.append(int(res.ans3))
            if res.ans4 is not None:
                content.append(int(res.ans4))
            if res.ans5 is not None:
                content.append(int(res.ans5))
            if res.ans6 is not None:
                content.append(int(res.ans6))
            if res.ans7 is not None:
                content.append(int(res.ans7))
            if res.ans8 is not None:
                content.append(int(res.ans8))
            tmp = {
                "content": content
            }
            answer.append(tmp)
            ans = []
            if question.content_1_isTrue == 1:
                ans.append(0)
            if question.content_2_isTrue == 1:
                ans.append(1)
            if question.content_3_isTrue == 1:
                ans.append(2)
            if question.content_4_isTrue == 1:
                ans.append(3)
            if question.content_5_isTrue == 1:
                ans.append(4)
            if question.content_6_isTrue == 1:
                ans.append(5)
            if question.content_7_isTrue == 1:
                ans.append(6)
            if question.content_8_isTrue == 1:
                ans.append(7)
            flag = 1
            if len(ans) != len(content):
                flag = 0
            else:
                for i in range(len(ans)):
                    if ans[i] != content[i]:
                        flag = 0
            if flag == 1:
                score += question.score
                rightNum += 1
        if res_build.que_type == "pack":
            res = Pack_ans.objects.get(pack_id=res_build.que_id)
            question = Pack.objects.get(pack_id=build.que_id)
            content = []
            if res.ans1 is not None:
                content.append((res.ans1))
            if res.ans2 is not None:
                content.append((res.ans2))
            if res.ans3 is not None:
                content.append((res.ans3))
            if res.ans4 is not None:
                content.append((res.ans4))
            if res.ans5 is not None:
                content.append((res.ans5))
            tmp = {
                "content": content
            }
            answer.append(tmp)
            ans = []
            if question.pack_ans_1 is not None:
                ans.append(question.pack_ans_1)
            if question.pack_ans_2 is not None:
                ans.append(question.pack_ans_2)
            if question.pack_ans_3 is not None:
                ans.append(question.pack_ans_3)
            if question.pack_ans_4 is not None:
                ans.append(question.pack_ans_4)
            if question.pack_ans_5 is not None:
                ans.append(question.pack_ans_5)
            flag = 1
            if len(ans) != len(content):
                flag = 0
            else:
                for i in range(len(ans)):
                    if ans[i] != content[i]:
                        flag = 0
            if flag == 1:
                score += question.score
                rightNum += 1
    result.score = score
    result.save()
    group = Result.objects.filter(list_id=list_id).order_by("-score")
    totalAnswerNum = Result.objects.filter(list_id=list_id).count()
    i = 0
    for x in group:
        if x.result_id == result.result_id:
            rank = i+1
        i += 1
    ret_data = {
        "totalAnswerNum": totalAnswerNum,
        "totalQueNum": question_num,
        "totalScore": tot_score,
        "score": score,
        "rank": rank,
        "rightNum": rightNum,
        "answer": answer
    }
    return JsonResponse(ret_data)


def time_line(request):
    list_id = request.GET.get("list_id")
    date_dic = {}
    today = datetime.datetime.now().date()
    create_day = List.objects.get(list_id=list_id).create_time.date()
    if today - create_day > datetime.timedelta(days=7):
        first_day = today - datetime.timedelta(days=7)
    else:
        first_day = create_day
    while first_day <= today:
        # print(first_day.strftime('%Y-%m-%d'))
        """
        if Result.objects.filter(submit_time__range=[first_day, first_day + datetime.timedelta(days=1)]) is not None:
        """
        # print(List.objects.filter(create_time__range=[first_day, first_day + datetime.timedelta(days=1)]))
        date_dic[first_day.strftime('%Y-%m-%d')] = Result.objects.filter(
            Q(submit_time__range=[first_day, first_day + datetime.timedelta(days=1)]) &
            Q(list_id=list_id)
        ).count()
        first_day += datetime.timedelta(days=1)
    ret_data = {
        "date_dic": date_dic
    }
    return JsonResponse(ret_data)
