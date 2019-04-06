from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

user_dic = {'username': 'cqh', 'passwd': '123'}

class IndexView(APIView):
    def get(self, request):
        # 渲染一个未登录状态的网页页面
        return render(request, 'index.html', locals())


class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html', locals())

    def post(self, request):
        response_dic = {'status': 'ok', 'msg': '登录成功'}
        username = request.POST.get('username', None)
        passwd = request.POST.get('passwd', None)
        if username == user_dic['username'] and passwd == user_dic['passwd']:
            pass
        else:
            response_dic['msg'] = '账户或密码错误,请重新登录'
        return Response(response_dic)


class UserInfo(APIView):
    def get(self, request):
        return render(request, 'user/user_info.html', locals())


class OrderList(APIView):
    def get(self, request):
        return render(request, 'order-list.html', locals())


def error404(request):
    return render(request, 'error404.html', locals())