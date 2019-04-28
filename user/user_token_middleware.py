import json
from django.utils.deprecation import MiddlewareMixin


# 在中间件的最后一层,将token取出,如果没有,request中的token字段置为None,方便后续直接取值判断
class UserTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # print(request.__dict__)
        request.token = request.COOKIES.get('token')
        # print(' 内部的token', request.token)

        # 放在头部的字段中,中划线会被自动转成下划线,并且会在开头自动加上HTTP_,并且转换成全大写字符串
        # print('中间件中',request.token)