from django.utils.deprecation import MiddlewareMixin
from owner.models import *
from django.http import JsonResponse


class Verify(MiddlewareMixin):
    def process_request(self, request):
        id = request.headers.get("Authorization")
        if id != "0":
            tmp = User.objects.filter(user_id=id)
            if not tmp.exists():
                ret_data = {
                    "message": "无权限访问"
                }
                return JsonResponse(ret_data)
