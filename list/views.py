from django.http import JsonResponse
from list.models import *


def add_list(request):
    new_list = List()
    new_list.state = request.Get.get("state")
    new_list.list_type = request.Get.get("list_type")
    new_list.list_name = request.Get.get("list_name")
    new_list.full_time = request.Get.get("full_time")
    new_list.start_time = request.Get.get("start_time")
    new_list.end_time = request.Get.get("end_time")
    new_list.last_edit_time = request.Get.get("last_edit_time")
    new_list.owner_id = request.Get.get("owner_id")
    new_list.que_num = request.Get.get("que_num")
    new_list.summary = request.Get.get("summary")

    new_list.save()
