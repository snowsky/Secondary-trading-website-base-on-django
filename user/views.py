import re
import redis
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from user import models
from user.salt_user_auth import UserGetCode
# 引入网易云信API,发送和验证短信
from user.sms import NeteaseSmsAPI
from user.my_redis_tool import POOL


class IndexView(APIView):
    def get(self, request):
        # 渲染一个未登录状态的网页页面
        return render(request, 'index.html', locals())


class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html', locals())

    def post(self, request):
        response_dic = {'status': 100, 'msg': '登录成功'}
        telephone = request.POST.get('telephone', None)
        passwd = request.POST.get('passwd', None)
        if not (telephone and passwd):
            response_dic['msg'] = '登录失败'
        else:
            user = models.User.objects.filter(telephone=telephone, password=passwd).first()
            print(isinstance(user, models.User))
            if not isinstance(user, models.User):
                response_dic['status'] = 100
                response_dic['msg'] = '账户或密码错误,请重新登录'
            else:
                response_dic['status'] = 200
        return Response(response_dic)


class RegisterView(APIView):
    def post(self, request):
        response_dic = {'status': 100, 'msg': '注册成功'}
        username = request.POST.get('username', None)
        passwd = request.POST.get('passwd', None)
        telephone = request.POST.get('telephone', None)
        code = request.POST.get('code', None)
        # email = request.POST.get('email', None)
        # email_reg = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        telephone_reg = r'^1[3|4|5|7|8][0-9]{9}$'
        # 值不全的时候不注册,返回失败

        # if not (username and passwd and telephone and email):
        if not (username and passwd and telephone):
            response_dic['status'] = 102
            response_dic['msg'] = '注册失败'
            print('缺少信息')
        elif len(username) < 6 or len(username) > 20 or len(passwd) < 6 or len(passwd) > 20:
            response_dic['status'] = 102
            response_dic['msg'] = '注册失败'
            print('密码或账户长度错误')
        # elif not (re.match(email_reg, email) and re.match(telephone_reg, telephone)):
        elif not re.match(telephone_reg, telephone):
            response_dic['status'] = 102
            response_dic['msg'] = '注册失败'
            print('手机格式错误')
        else:
            # 短信验证
            try:
                # models.User.objects.create(username=username, password=passwd, email=email, telephone=telephone)
                models.User.objects.create(username=username, password=passwd, telephone=telephone)
            except Exception as e:
                print(e)
                response_dic['status'] = 101
                response_dic['msg'] = '用户已存在'
        return Response(response_dic)


class UserInfo(APIView):
    def get(self, request):
        return render(request, 'user/user_info.html', locals())


class OrderList(APIView):
    def get(self, request):
        return render(request, 'order-list.html', locals())


def error404(request):
    return render(request, 'error404.html', locals())


class ContactMe(APIView):
    def get(self, request):
        return render(request, 'contact_me.html', locals())


class GetCode(APIView):
    throttle_classes = [UserGetCode]

    def post(self, request):
        response_dic = {'status': 101, 'msg': '获取验证码失败'}

        if request.method == 'POST':
            telephone = request.POST.get('telephone', None)
            if telephone:
                print(telephone)
                try:
                    # 设置频率器,控制发送的频率
                    # 调用网易云信接口给获取到的手机号
                    response_dic['status'] = 200
                    sms_api = NeteaseSmsAPI()
                    res = sms_api.send_code(telephone)
                    conn = redis.Redis(connection_pool=POOL)
                    conn.hset(telephone, {'msg': res['msg'], 'code': res['obj']})
                    response_dic['status'] = 200
                    response_dic['msg'] = '获取验证码成功'
                    return Response(response_dic)
                    # 直接把网易云信接口的返回数据返回
                except Exception as e:
                    print(e)
                    return Response(response_dic)

            return Response(response_dic)