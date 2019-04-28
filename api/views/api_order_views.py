from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from good.models import Good, GoodStatusAndSellMethod
from order.models import OrderStatusAndBillStatus, Order, Delivery
from user.models import User, UserAddress
from order.utils.order_ser import SaveOrderSerializer, OrderSerializer
from user.utils.user_address_ser import UserAddressSerializer
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
            good_id = request.POST.get('good', None)
            good_obj = Good.objects.get(pk=good_id)
            # 当前买家不能是商品的拥有者,且不是卖家
            # print(good_obj.owner_user_id)
            # print(request.POST.get('seller', None))
            # print(str(request.POST.get('buyer', None) != str(good_obj.owner_user_id)))
            if str(request.POST.get('buyer', None)) != str(good_obj.owner_user_id):
                # good_obj = Good.objects.get(pk=good_id)
                # print(good_obj.good_status.status_content)

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


# 获取用户买下的商品(已加入drf分页器)
class GetBuyOrder(APIView):
    authentication_classes = [UserTokenAuth]

    def get(self, request):
        response = CommonResponse()
        try:
            order_list = Order.objects.filter(good__order__buyer_id=request.user_id).all()
            if order_list:
                # response.data = {'order_list': {}}

                # 创建分页器对象
                page = OrderPage()

                page_list = page.paginate_queryset(order_list, request, view=self)
                order_ser = OrderSerializer(instance=page_list, many=True)

                return page.get_paginated_response(order_ser.data)

                # for item in order_list:
                #     order_ser = OrderSerializer(instance=item)
                #     # print(order_ser.data)
                #     # print(order_ser.data)
                #     response.data['order_list'][item.id] = {**order_ser.data}
                #     response.msg = '获取买入商品订单成功'
                #     response.status = 200
            else:
                response.msg = '没有买入商品的订单'
        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())


# 获取用户卖出的商品(已加入drf分页器)
class GetSellOrder(APIView):
    authentication_classes = [UserTokenAuth]

    def get(self, request):
        response = CommonResponse()
        try:
            order_list = Order.objects.filter(good__order__seller_id=request.user_id).all()

            if order_list:
                # response.data = {'order_list': {}}

                # 创建分页对象
                page = OrderPage()

                # 在数据库中获取分页的数据
                page_list = page.paginate_queryset(order_list, request, view=self)

                order_ser = OrderSerializer(instance=page_list, many=True)

                return page.get_paginated_response(order_ser.data)

                # for item in page_list:
                #     order_ser = OrderSerializer(instance=item)
                #     response.data['order_list'][item.id] = {**order_ser.data}
                #     response.status = 200
                #     response.msg = '查询卖出订单成功'
            else:
                response.msg = '没有卖出的订单'
        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())


# 对分页器类的单独设置
class OrderPage(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 5


# 卖家发货接口
# 需要在url中传递订单id,data中传递
class SellerSendDelivery(APIView):
    authentication_classes = [UserTokenAuth]

    #
    # def get(self, request):
    #     return HttpResponse('进入接口的get方法')

    def post(self, request, order_id):
        print('======================进入了post请求中========')
        response = CommonResponse()
        try:
            order_obj = Order.objects.get(pk=order_id)

            # 判断用户是卖家,才能发货
            if request.user_id == order_obj.seller_id:
                pay_status = OrderStatusAndBillStatus.objects.get(status_content='买家已付款')
                can_delivery_status = OrderStatusAndBillStatus.objects.get(status_content='卖家未发货')
                delivert_status = OrderStatusAndBillStatus.objects.get(status_content='卖家已发货')
                # 判断订单是否买家已付款,已付款才能发货
                if order_obj.bill_status == pay_status and order_obj.order_status == can_delivery_status:
                    # 根据原订单买家的收货地址+卖家传来的收货地址id,生成快递单
                    buyer_address_obj = UserAddress.objects.get(pk=order_obj.buyer_address_id)
                    seller_address_id = request.POST.get('seller_address_id', None)
                    seller_address_obj = UserAddress.objects.get(pk=seller_address_id)
                    if seller_address_obj:

                        buyer_address_ser = UserAddressSerializer(instance=buyer_address_obj)
                        seller_address_ser = UserAddressSerializer(instance=seller_address_obj)
                        print(buyer_address_ser.data)
                        print(seller_address_ser.data)

                        with transaction.atomic():
                            delivery_obj = Delivery.objects.create(
                                delivery_company=request.POST.get('delivery_company'),
                                receiver_address=buyer_address_ser.data['receiver_address'],
                                receiver_name=buyer_address_ser.data['receiver_name'],
                                receiver_telephone=buyer_address_ser.data['receiver_telephone'],
                                sender_address=seller_address_ser.data['receiver_address'],
                                sender_telephone=seller_address_ser.data['receiver_telephone'],
                                sender_name=seller_address_ser.data['receiver_name'])
                            if delivery_obj:
                                # 将快递单信息保存到对应的订单中
                                order_obj.delivery = delivery_obj
                                order_obj.seller_address = seller_address_obj
                                order_obj.order_status = delivert_status
                                order_obj.save()
                                response.msg = '快递单生成成功'

                            else:
                                response.msg = '订单生成失败'
                    else:
                        response.msg = '卖家地址不存在'
                else:
                    response.msg = '当前订单状态不能发货'
            else:
                response.msg = '您不是商品的卖家,不能发货'
                response.status = 101
        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())


# 买家收货接口,卖家发货且买家已付款的订单才可以进行操作,并且订单对应金额打入用户的balance中
class BuyerReceiveDelivery(APIView):
    authentication_classes = [UserTokenAuth]

    def post(self, request, order_id):
        response = CommonResponse()
        try:
            order_obj = Order.objects.get(pk=order_id)
            # 有订单且当前登录用户是买家才可以修改状态
            # print(str(order_obj.buyer_id) == str(request.user_id),'++++++++++++++++')
            if order_obj and (str(order_obj.buyer_id) == str(request.user_id)):
                # 判断订单状态,是买家已付款,卖家已发货的订单,才可以继续做收货操作
                buy_status = OrderStatusAndBillStatus.objects.get(status_content='买家已付款')
                can_receive_status = OrderStatusAndBillStatus.objects.get(status_content='卖家已发货')
                if order_obj.bill_status == buy_status and order_obj.order_status == can_receive_status:
                    # 订单状态是可以收货的状态,修改订单为买家已收货,卖家已收款,并且修改卖家账户余额,将订单金额加进用户账户

                    bill_complete_status = OrderStatusAndBillStatus.objects.get(status_content='卖家已收款')
                    receive_complete_status = OrderStatusAndBillStatus.objects.get(status_content='买家已收货')
                    seller_obj = User.objects.get(pk=order_obj.seller_id)
                    with transaction.atomic():
                        order_obj.bill_status = bill_complete_status
                        order_obj.order_status = receive_complete_status
                        seller_obj.balance += float(order_obj.order_price)
                        order_obj.save()
                        seller_obj.save()
                        response.msg = '买家收货成功,钱款已打入卖家余额中'

                else:
                    response.msg = '订单当前状态不能做收货操作'

            else:
                response.msg = '没有该订单或您不是订单的买家'
                response.status = 101
        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())


# 买家收货后,申请退款的接口,只有订单状态,卖家已收款,买家已收货的订单,可以由买家申请退款
class BuyerMotionDrawback(APIView):
    authentication_classes = [UserTokenAuth]

    def post(self, request, order_id):
        response = CommonResponse()
        try:
            order_obj = Order.objects.get(pk=order_id)
            # 确认订单存在,并且当前用户是买家
            if order_obj and (str(request.user_id) == str(order_obj.buyer_id)):
                # 查出可以操作的订单状态,用来对当前订单做判断使用
                bill_status = OrderStatusAndBillStatus.objects.get(status_content='卖家已收款')
                order_status = OrderStatusAndBillStatus.objects.get(status_content='买家已收货')
                if order_obj.bill_status == bill_status and order_obj.order_status == order_status:
                    bill_drawback_status = OrderStatusAndBillStatus.objects.get(status_content='买家已申请退款')
                    seller_obj = User.objects.get(pk=order_obj.seller_id)
                    if seller_obj:
                        if float(seller_obj.balance) >= float(order_obj.order_price):
                            seller_obj.balance = float(seller_obj.balance) - float(order_obj.order_price)
                            order_obj.bill_status = bill_drawback_status
                            with transaction.atomic():
                                order_obj.save()
                                seller_obj.save()
                                response.msg = '买家申请退款成功,请前往发送快递'

                        else:
                            response.msg = '请联系卖家从其他方式退款'

                    else:
                        response.msg = '无法找到当前订单的买家信息'

                else:
                    response.msg = '订单当前状态无法申请退款'

            else:
                response.msg = '该订单不存在或您不是订单的买家'
        except Exception as e:
            response.msg = str(e)

        return Response(response.get_dic())


# 买家申请退款成功后,进行退货发货的操作接口
# 订单状态是买家已申请退款且买家已收货状态的订单才能操作
# 需要传递数据drawback_delivery_price退货单运费价格,delivery_company快递公司
class BuyerSendDrawbackDelivery(APIView):
    authentication_classes = [UserTokenAuth]

    def post(self, request, order_id):
        response = CommonResponse()

        order_obj = Order.objects.get(pk=order_id)
        # 只有当前用户是订单的买家才可以操作
        if order_obj and (str(order_obj.buyer_id) == str(request.user_id)):
            # 订单状态必须是买家已申请退款且买家已收货的订单才可以发退货单
            bill_status = OrderStatusAndBillStatus.objects.get(status_content='买家已申请退款')
            order_status = OrderStatusAndBillStatus.objects.get(status_content='买家已收货')
            print(order_obj.bill_status == bill_status)
            print(order_obj.order_status == order_status)
            if (order_obj.bill_status == bill_status) and (order_obj.order_status == order_status):
                order_send_drawback_delivery = OrderStatusAndBillStatus.objects.get(status_content='买家已退货')
                # 要生成一个退货的快递单,并保存一个外键在退货的订单中
                drawback_delivery_price = request.POST.get('drawback_delivery_price', None)
                buyer_address_obj = UserAddress.objects.get(pk=order_obj.buyer_address_id)
                seller_address_obj = UserAddress.objects.get(pk=order_obj.seller_address_id)
                buyer_address_ser = UserAddressSerializer(instance=buyer_address_obj)
                seller_address_ser = UserAddressSerializer(instance=seller_address_obj)
                with transaction.atomic():
                    # 将买家卖家的地址互换发收件人位置后,生成退货运单
                    drawback_delivery_obj = Delivery.objects.create(
                        delivery_company=request.POST.get('delivery_company'),
                        receiver_address=seller_address_ser.data['receiver_address'],
                        receiver_name=seller_address_ser.data['receiver_name'],
                        receiver_telephone=seller_address_ser.data['receiver_telephone'],
                        sender_address=buyer_address_ser.data['receiver_address'],
                        sender_telephone=buyer_address_ser.data['receiver_telephone'],
                        sender_name=buyer_address_ser.data['receiver_name'])
                    if drawback_delivery_obj:
                        # 修改订单的状态,将退货单关联进用户
                        order_obj.drawback_delivery = drawback_delivery_obj
                        order_obj.drawback_delivery_price = drawback_delivery_price
                        order_obj.order_status = order_send_drawback_delivery
                        order_obj.save()
                        response.msg = '退货操作成功,已生成退货运单并修改订单信息'

                    else:
                        response.msg = '生成退货运单失败,请重试'
            else:
                response.msg = '订单当前状态不能进行退货操作'

        else:
            response.msg = '该订单不存在或你不是订单的买家,无法操作'

        return Response(response.get_dic())


# 买家退货发货成功后,卖家收货退款给买家的接口
class SellerReceiveDeliveryDrawback(APIView):

    authentication_classes = [UserTokenAuth]

    def post(self, request, order_id):
        response = CommonResponse()
        order_obj = Order.objects.get(pk=order_id)
        # 只有订单存在且用户是卖家时可以操作
        if order_obj and str(request.user_id) == str(order_obj.seller_id):
            # 判断订单状态为买家已申请退款且买家已退货,才可以操作订单的状态
            bill_status = OrderStatusAndBillStatus.objects.get(status_content='买家已申请退款')
            order_status = OrderStatusAndBillStatus.objects.get(status_content='买家已退货')
            if order_obj.bill_status == bill_status and order_obj.order_status == order_status:
                # 修改订单状态,将钱款转回买家的账户余额中
                bill_complete_status = OrderStatusAndBillStatus.objects.get(status_content='卖家已退款')
                order_complete_status = OrderStatusAndBillStatus.objects.get(status_content='卖家已收货')
                buyer = User.objects.get(pk=order_obj.buyer_id)
                buyer.balance = float(buyer.balance) + float(order_obj.order_price)
                order_obj.bill_status = bill_complete_status
                order_obj.order_status = order_complete_status
                # 数据库事务操作 保证原子性
                with transaction.atomic():
                    order_obj.save()
                    buyer.save()

                    response.msg = '订单卖家收货退款操作已完成'

            else:
                response.msg = '当前订单状态无法进行卖家的收货退款操作'

        else:
            response.msg = '该订单不存在或你不是卖家,无法操作'

        return Response(response.get_dic())