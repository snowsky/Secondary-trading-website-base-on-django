# 用于用户操作除注册登录页面外的页面时的身份验证
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import redis

from user.utils.my_redis_tool import POOL
from user.models import User


class UserTokenAuth(BaseAuthentication):
    def authenticate(self, request):
        # 对于get请求也要做验证,不然之后获取了网页,传来的信息不知道是谁在操作
        # if request.method != 'GET':
        token = request.token
        print(token)
        conn = redis.Redis(connection_pool=POOL)
        keys = conn.keys()
        # 将keys从bytes转成str类型
        keys = [str(key, encoding='utf-8') for key in keys]
        if token in keys:
            user_id = conn.get(token)
            try:
                user = User.objects.filter(id=user_id).first()
            except Exception as e:
                raise AuthenticationFailed('认证失败')
            if user:
                request.user_id = user.id
                return user, token

        raise AuthenticationFailed('认证失败')

    def authenticate_header(self, request):
        pass