import json
import re

import redis
from django.shortcuts import render, HttpResponse
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
from dwebsocket import accept_websocket
from user.models import User

request_websocket_list = []


# websocket用的视图函数
@accept_websocket
def web_chat(request, good_id):
    if not request.is_websocket():
        try:
            print(request.data)
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'web_cheat.html', locals())

    # websocket的消息都会到这里,所以可以在此处理逻辑
    else:
        print('发来的是websocket请求')

        # 只有是websocket消息,就要循环等待
        while True:
            # 消息的等待一定要放在最开始,放在判断逻辑中的话,会导致前台与后台的连接断开
            print('开始消息等待')
            # 第一次连接的时候,如果有带token,就可以直接保存用户了

            # 没有token,就等下次发消息的时候再保存用户

            token = request.token
            # print('token', token)

            # 只有token有值的时候,才好进行用户状态的保存和消息的转发
            # 链接redis是为了根据token取到redis中的user_id
            # 只有带着token来了,才能做下面的保存用户的操作
            if token:
                # 链接redis
                from user.utils.my_redis_tool import POOL
                import redis
                conn = redis.Redis(connection_pool=POOL)

                # 根据token获取用户id
                user_id = str(conn.get(token), encoding='utf-8')

                # 即使带了token,但是redis中没有该token对应用户的登录记录,也一样不算用户已登录,需要先登录
                if user_id:
                    sender_user = User.objects.get(pk=int(user_id))
                    print('sender_user', sender_user)

                    # 将当前的连接者的用户id,及它的websockt对象,保存成一个列表,保存进我们的列表
                    web_element = [user_id, request.websocket]
                    # print('web_element', web_element)
                    # print(request_websocket_list)
                    for item in request_websocket_list:
                        # print(item)
                        if str(item[0]) == str(user_id):
                            item[1] = request.websocket
                            break
                    else:
                        request_websocket_list.append(web_element)

            print(request_websocket_list)

            # 如果刚连接时就带了token,就在上面保存发送的用户
            # 如果没有带token也没关系,先让用户连接到服务器,再次发送消息时提示报错
            message = request.websocket.wait()
            # try:
            print('request.websocket', request.websocket)

            # 进到websocket请求的第一步要判断当前请求的用户有没有登录,先判断有没有带token
            # 再判断token在redis中有木对应用户id
            # 得到当前链接者,即消息发送者的token
            token = request.token
            # print('token', token)

            # 只有token有值的时候,才好进行用户状态的保存和消息的转发
            # 链接redis是为了根据token取到redis中的user_id
            # 只有带着token来了,才能做下面的保存用户的操作
            if token:
                # 链接redis
                from user.utils.my_redis_tool import POOL
                import redis
                conn = redis.Redis(connection_pool=POOL)

                # 根据token获取用户id
                user_id = str(conn.get(token), encoding='utf-8')

                # 即使带了token,但是redis中没有该token对应用户的登录记录,也一样不算用户已登录,需要先登录
                if not user_id:
                    back_message = '您当前还未登录,请登录后再发消息'
                    request.websocket.send(bytes(back_message, encoding='utf-8'))
                    return

            else:
                back_message = '您当前还未登录,请登录后再发消息,已断开服务器连接,请登录连接重试'
                request.websocket.send(bytes(back_message, encoding='utf-8'))
                return

            # 在确认用户登录后,进到websocket请求的第二步就是保存当前链接用户的id和websocket对象
            # 获取发送者对象,根据token获取到的user_id
            sender_user = User.objects.get(pk=int(user_id))
            print('sender_user', sender_user)

            # 将当前的连接者的用户id,及它的websockt对象,保存成一个列表,保存进我们的列表
            web_element = [user_id, request.websocket]
            # print('web_element', web_element)
            print(request_websocket_list)
            for item in request_websocket_list:
                # print(item)
                if str(item[0]) == str(user_id):
                    item[1] = request.websocket
                    break
            else:
                request_websocket_list.append(web_element)

            print('request_list', request_websocket_list)

            # 至此将已连接用户保存下来的工作完成

            # 接下来是把sender发来的信息拆分,找出消息的receiver,和真实发送的内容

            # 然后将消息发给真正的消息接受者
            # request.websocket.send(message)
            # print('request_websocket_set', request_websocket_set)
            print('等待发来消息')

            # message = request.websocket.wait()

            # 接收到的message是bytes类型,转成字符串
            if not message:
                continue
            str_message = str(message, encoding='utf-8')

            # print(str_message)

            # 拆分字符串格式的消息
            send_message = str_message.split(':')[1]
            print('send_message', send_message)

            # 切分要发给的用户的名字
            receiver_name = str_message.split(':')[0]
            print('receiver_name', receiver_name)

            # 根据切分的用户名,查找接受者对象
            try:
                receiver_obj = User.objects.get(username=receiver_name)

                # 只有有这个用户才可能发送
                if receiver_obj:
                    # 遍历request_websocket_list列表
                    for item in request_websocket_list:
                        if str(item[0]) == str(receiver_obj.id):
                            item[1].send(bytes(send_message, encoding='utf-8'))
                            print('消息发送给{},成功'.format(receiver_obj.username))

                            # 消息发送成功了,要将消息记录也保存进数据库中
                            from user.models import ChatRecord
                            from good.models import Good
                            good_obj = Good.objects.get(pk=good_id)
                            ChatRecord.objects.create(good=good_obj, sender=sender_user, receiver=receiver_obj,
                                                      content=send_message)

                            break
                else:
                    back_message = '你要发送的用户不存在,请修改后重新发送'
                    request.websocket.send(bytes(back_message, encoding='utf-8'))

            except Exception as e:
                back_message = str(e)
                request.websocket.send(bytes(back_message, encoding='utf-8'))

        #         else:
        #             back_message = '你要发送的用户不存在,请修改'
        #             request.websocket.send(bytes(back_message, encoding='utf-8'))
        #
        # else:
        #     back_message = '你当前还未登录,请先登录'
        #     request.websocket.send(bytes(back_message, encoding='utf-8'))
        #     return

        # except Exception as e:
        #     back_message = str(e)
        #     request.websocket.send(bytes(back_message, encoding='utf-8'))


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
