from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.conf import settings
from user.utils.common_response import CommonResponse
from user.utils.user_address_ser import UserAddressSerializer
from user.utils.user_drf_auth import UserTokenAuth


class AddAddress(APIView):

    authentication_classes = [UserTokenAuth]

    def get(self, request):
        return HttpResponse('这里返回填写地址的页面')

    # 接受用户发来的地址信息
    def post(self, request):
        """
        receiver_name = models.CharField(max_length=64, verbose_name='收件人姓名')
    receiver_telephone = models.BigIntegerField(verbose_name='收件人手机')
    receiver_address = models.TextField(verbose_name='收件人地址')
    # 加一个外键关联用户表
    user = models.ForeignKey(to='User', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='用户')

        :param request:
        :return:
        """
        # 准备序列化组件
        response = CommonResponse()

        user_address_ser = UserAddressSerializer(data=request.data)
        print('=======================', user_address_ser.is_valid())
        if user_address_ser.is_valid():

            if str(request.user_id) == request.data['user']:
                user_address_obj = user_address_ser.save()

                response = CommonResponse()
                response.msg = '地址保存成功'
            else:
                response.msg = '需要本人添加地址'
        else:
            response.msg = '数据格式错误'

        return Response(response.get_dic())


