import json
import re

import redis
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from user import models
from user.utils.salt_user_auth import UserGetCode
# 引入网易云信API,发送和验证短信
from user.sms import NeteaseSmsAPI
from user.utils.my_redis_tool import POOL
from user.utils.common_response import CommonResponse
from user.utils.token_value_calc import CheckUserToken
from user.utils.user_form import LoginCheckForm, RegisterCheckForm


class IndexView(APIView):
    def get(self, request):
        # 渲染一个未登录状态的网页页面
        return render(request, 'index.html', locals())


from django.views.decorators.csrf import csrf_exempt


# 用户登录接口


class LoginView(APIView):
    # get请求返回登录页面
    def get(self, request):
        return render(request, 'login.html', locals())

    # post请求接受数据并开始用户登录的校验功能
    @csrf_exempt
    def post(self, request):
        print('开始验证')
        response = CommonResponse()
        check_form = LoginCheckForm(request.POST)
        if check_form.is_valid():
            # 获取客户端传来的token
            client_token = request.token
            print(client_token)
            # print('token', client_token)
            # 建立redis连接
            conn = redis.Redis(connection_pool=POOL)
            # 获取服务器端token
            try:
                keys = conn.keys()
                keys = [str(key, encoding='utf-8') for key in keys]
                # print('client_token', client_token)
                # print('keys', keys)
                # print(keys[3])
                # print('status', client_token in keys)
                # print()

            except Exception as e:
                print(e)
                keys = None

            # 如果存在token,就不再验证用户密码,直接通过了
            if client_token in keys:

                response.status = 200
                response.msg = '登录成功'
                response.data = {'salt_cookie': client_token}

            # 如果客户端或服务器端有一方没有token的时候,直接根据手机号和密码登录
            elif (not client_token) or (client_token not in keys):
                telephone = request.POST.get('telephone', None)
                passwd = request.POST.get('passwd', None)
                print(telephone)
                print(passwd)
                if not (telephone and passwd):
                    response.msg = '登录失败'
                else:
                    user = models.User.objects.filter(telephone=telephone, password=passwd).first()
                    # 如果查询成功,表示信息正确,生成token值
                    # if isinstance(user, models.User):
                    if user:
                        # 设置返回json的状态
                        response.status = 200
                        response.msg = '登录成功'
                        # 生成token的函数做成类
                        token_api = CheckUserToken()
                        token_str = token_api.get_token_str(telephone)
                        # 并设置过期时间,放在redis中
                        conn = redis.Redis(connection_pool=POOL)
                        # 在redis保存什么数据?
                        conn.set(token_str, user.id, ex=86400)

                        response.data = {'salt_cookie': token_str}
                    else:
                        response.msg = '账户或密码错误,请重新登录'

            # 客户端和服务器都带有token数据时,做校验,如果校验失败,不在验证用户,跳转登录信息
            else:
                response.msg = '登录失败'
        else:
            response.status = 101
            response.msg = '注册失败,信息格式不正确'

        return Response(response.get_dic())


class RegisterView(APIView):
    def post(self, request):

        response = CommonResponse()
        check_form = RegisterCheckForm(request.POST)
        print(request.POST)
        print(check_form.is_valid())
        if check_form.is_valid():
            username = request.POST.get('username', None)
            passwd = request.POST.get('passwd', None)
            telephone = request.POST.get('telephone', None)
            code = request.POST.get('code', None)
            print(username)
            print(code)

            # email = request.POST.get('email', None)
            # email_reg = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
            # telephone_reg = r'^1[3|4|5|7|8][0-9]{9}$'
            # 值不全的时候不注册,返回失败
            # if not (username and passwd and telephone and email):
            # if not (username and passwd and telephone):
            #     response.status = 102
            #     response_dic['msg'] = '注册失败'
            #     print('缺少信息')
            # elif len(username) < 6 or len(username) > 20 or len(passwd) < 6 or len(passwd) > 20:
            #     response_dic['status'] = 102
            #     response_dic['msg'] = '注册失败'
            #     print('密码或账户长度错误')
            # # elif not (re.match(email_reg, email) and re.match(telephone_reg, telephone)):
            # elif not re.match(telephone_reg, telephone):
            #     response_dic['status'] = 102
            #     response_dic['msg'] = '注册失败'
            #     print('手机格式错误')
            # else:

            # 服务器端短信验证码的获取
            conn = redis.Redis(connection_pool=POOL)
            redis_code = conn.get(telephone)
            if redis_code:
                redis_code = str(int(redis_code))
                print('code', code)
                # 验证码匹配成功
                if redis_code == code:
                    print('匹配成功')

                    try:
                        # models.User.objects.create(username=username, password=passwd, email=email, telephone=telephone)
                        models.User.objects.create(username=username, password=passwd, telephone=telephone, user_type=0)
                        response.status = 100
                        response.msg = '注册成功'
                    except Exception as e:
                        print(e)
                        response.status = 100
                        response.msg = '用户已存在'

                # 验证码匹配失败
                else:
                    response.status = 101
                    response.msg = '验证码错误'
            # 没有获取过验证码
            else:
                response.status = 101
                response.msg = '请重新获取验证码'
        else:
            response.status = 101
            response.msg = '信息格式错误'

        return Response(response.get_dic())


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
        if request.is_ajax():
            response_dic = {'status': 101, 'msg': '获取验证码失败'}
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
                    conn.set(telephone, res['obj'], ex=1800)
                    response_dic['status'] = 200
                    response_dic['msg'] = '获取验证码成功'
                    # print('obj', res['obj'])
                    return Response(response_dic)
                except Exception as e:
                    print(e)
                    return Response(response_dic)

            return Response(response_dic)
