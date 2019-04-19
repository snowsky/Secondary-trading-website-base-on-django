from rest_framework.response import Response
from rest_framework.views import APIView

from good.models import Good, GoodStatusAndSellMethod
from order.models import OrderStatusAndBillStatus, Order
from order.utils.order_ser import SaveOrderSerializer, OrderSerializer
# from django.conf import settings
from user.utils.common_response import CommonResponse
from user.utils.user_drf_auth import UserTokenAuth
from django.db import transaction


# 查出所有订单和钱款状态数据 返回给前台
class GetOrderStatusAndBillStatus(APIView):
    authentication_classes = [UserTokenAuth]

    def get(self, request):
        response = CommonResponse()
        response.data = {'order_bill_status_list': {}}
        order_bill_status_list = OrderStatusAndBillStatus.objects.all()
        for item in order_bill_status_list:
            response.data['order_bill_status_list'][item.id] = item.status_content

        response.msg = '获取订单和钱款信息成功'
        return Response(response.get_dic())


# 用于接受买单用户传来的数据,订单状态为买家未付款,卖家未发货,等待用户
# 返回json格式数据,status为200的时候可以在让前台跳转支付页面,其他状态让用户重新生成订单
class BuyByGoodId(APIView):
    authentication_classes = [UserTokenAuth]

    def post(self, request, good_id):
        """
        order_id = models.CharField(max_length=128, unique=True, verbose_name='订单号')
        order_title = models.TextField(verbose_name='商品标题')
        buyer = models.ForeignKey(to='user.User', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='买家')
        seller = models.ForeignKey(to='user.User', related_name='seller', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='卖家')
        order_status = models.ForeignKey(to='OrderStatusAndBillStatus', null=True, related_name='order_status', default=0, on_delete=models.SET_NULL, verbose_name='订单状态')
        bill_status = models.ForeignKey(to='OrderStatusAndBillStatus', related_name='bill_status', null=True, on_delete=models.SET_NULL, default=5, verbose_name='钱款状态')
        delivery_price = models.FloatField(verbose_name='运费')
        order_price = models.FloatField(verbose_name='订单金额')
        delivery = models.ForeignKey(to='Delivery', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='快递')
        created_time = models.DateField(auto_now_add=True, verbose_name='订单生成时间')
        good = models.ForeignKey(to='good.Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='订单对应商品')

        :param request:
        :param good_id:
        :return:
        """
        response = CommonResponse()
        try:
            response = CommonResponse()

            # 当前买家不能是卖家
            if request.user_id != request.POST.get('seller', None):
                good_obj = Good.objects.get(pk=good_id)
                print(good_obj.good_status.status_content)

                if good_obj.good_status.status_content == '已发布':
                    # 将post数据转成通过序列化组件转成对象
                    order_ser = SaveOrderSerializer(data=request.POST)

                    if order_ser.is_valid():
                        # ORM的事务操作原子化,一个出错全部撤回
                        with transaction.atomic():
                            order_obj = order_ser.save()

                            if order_obj:
                                good_buy_status = GoodStatusAndSellMethod.objects.get(status_content='交易中')
                                good_obj.good_status = good_buy_status
                                good_obj.save()
                                response.status = 200
                                response.msg = '订单生成成功'
                            else:
                                response.msg = '订单生成失败'
                    else:
                        response.msg = '订单数据有误'
                else:
                    response.msg = '当前商品不能购买'
            else:
                response.msg = '你不能买自己发布的商品'

        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())


# 供买家或卖家在自己的一端删除订单,即让订单不再显示
class EditOrder(APIView):

    authentication_classes = [UserTokenAuth]

    def delete(self, request, order_id):
        response = CommonResponse()
        # try:
        order_obj = Order.objects.get(pk=order_id)
        print(order_obj)
        if request.user_id == order_obj.buyer.id:
            order_obj.buyer_is_show = 0
            response.msg = '买家已将订单删除'
        elif request.user_id == order_obj.seller.id:
            order_obj.seller_is_show = 0
            response.msg = '卖家已将订单删除'
        else:
            response.msg = '用户身份校验失败'
            response.status = 101
        order_obj.save()
        # except Exception as e:
        #     response.msg = str(e)

        return Response(response.get_dic())


# 获取用户买下的商品(后续加入分页器)
class GetBuyOrder(APIView):
    authentication_classes = [UserTokenAuth]

    def get(self, request):
        response = CommonResponse()
        try:
            order_list = Order.objects.filter(good__order__buyer_id=request.user_id)
            if order_list:
                response.data = {'order_list': {}}
                for item in order_list:
                    order_ser = OrderSerializer(instance=item)
                    # print(order_ser.data)
                    # print(order_ser.data)
                    response.data['order_list'][item.id] = {**order_ser.data}
                    response.msg = '获取买入商品订单成功'
                    response.status = 200
            else:
                response.msg = '没有买入商品的订单'
        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())


# 获取用户卖出的商品(后续加入分页器)
class GetSellOrder(APIView):
    authentication_classes = [UserTokenAuth]

    def get(self, request):
        response = CommonResponse()
        try:
            order_list = Order.objects.filter(good__order__seller_id=request.user_id)

            if order_list:
                response.data = {'order_list': {}}

                for item in order_list:
                    order_ser = OrderSerializer(instance=item)
                    response.data['order_list'][item.id] = {**order_ser.data}
                    response.status = 200
                    response.msg = '查询卖出订单成功'
            else:
                response.msg = '没有卖出的订单'
        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())
