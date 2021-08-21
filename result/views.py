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
    #list = List.objects.get(list_id=result.list_id)
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
                result_build.list_id = result.result_id
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
                result_build.list_id = result.result_id
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
                result_build.list_id = result.result_id
                result_build.que_no = i+1
                result_build.que_type = type
                result_build.que_id = pack_ans.pack_id
                result_build.save()
            if type == "rate":
                rate_ans = Rate_ans()
                rate_ans.ans = answer.get("content")
                rate_ans.save()
                result_build = Result_build()
                result_build.list_id = result.result_id
                result_build.que_no = i+1
                result_build.que_type = type
                result_build.que_id = rate_ans.rate_id
                result_build.save()
    ret_data = {
        'message': "submit success"
    }
    return JsonResponse(ret_data, safe=False)