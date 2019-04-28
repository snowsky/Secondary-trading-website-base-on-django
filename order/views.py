from django.shortcuts import render, redirect, HttpResponse
from order.models import Order, OrderStatusAndBillStatus
from user.utils.common_response import CommonResponse
from order.keys.pay import AliPay
import time
from rest_framework.response import Response
import os
import redis
from user.utils.my_redis_tool import POOL
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = os.path.dirname(__file__)
host_url = 'www.iqer.info'
# host_url = '127.0.0.1'

def ali():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "写上你的支付宝appid"
    # 支付宝收到用户的支付,会向商户发两个请求,一个get请求,一个post请求
    # POST请求，用于最后的检测
    notify_url = "http://{}:80/order/page2/".format(host_url)
    # GET请求，用于页面的跳转展示
    return_url = "http://{}:80/order/page2/".format(host_url)
    # 用户私钥
    merchant_private_key_path = os.path.join(BASE_DIR, "keys/alipay_private_2048.txt")
    # 支付宝公钥
    alipay_public_key_path = os.path.join(BASE_DIR, "keys/alipay_public_2048.txt")
    # 生成一个AliPay的对象
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


def page1(request, order_id):
    if request.method == "GET":
        try:
            token = request.token
            print(token)
            conn = redis.Redis(connection_pool=POOL)
            keys = conn.keys()
            # 二进制数据转字符串
            keys = [str(key, encoding='utf-8') for key in keys]

            if token in keys:
                user_id = conn.get(token)
                user_id = str(user_id, encoding='utf-8')
                # print(user_id)

                order_obj = Order.objects.get(pk=order_id)  # type:Order

                if order_obj:
                    if str(order_obj.buyer_id) == user_id:
                        return render(request, 'pay/pay_page.html', locals())
                    else:
                        return HttpResponse('你不能购买自己的商品')

                else:
                    return HttpResponse('订单信息获取失败')
            else:
                return HttpResponse('请先登录')
        except Exception as e:
            return HttpResponse(str(e))

    else:
        # print(request.POST)
        print(order_id)
        money = float(request.POST.get('money'))
        order_obj = Order.objects.get(pk=order_id)
        # 生成一个对象
        alipay = ali()
        # 生成支付的url
        # 对象调用direct_pay
        # 该方法生成一个加密串
        query_params = alipay.direct_pay(
            subject=order_obj.order_title,  # 商品简单描述
            out_trade_no=order_obj.order_id,  # 商户订单号
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)

            # subject="充气娃娃",  # 商品简单描述
            # out_trade_no="x2" + str(time.time()),  # 商户订单号
            # total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        print(pay_url)
        # 朝这个地址发get请求
        # from django.http import JsonResponse
        # return JsonResponse({'status':100, 'url':pay_url})
        return redirect(pay_url)


@csrf_exempt
def page2(request):
    # 支付宝如果收到用户的支付,支付宝会给我的地址发一个post请求,一个get请求
    alipay = ali()
    if request.method == "POST":
        print('支付宝回调,post请求======================')
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        print(body_str)

        post_data = parse_qs(body_str)
        print('支付宝给我的数据:::---------',post_data)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print('转完之后的字典',post_dict)
        # 做二次验证
        sign = post_dict.pop('sign', None)
        # 通过调用alipay的verify方法去认证
        status = alipay.verify(post_dict, sign)

        print('POST验证', status)
        if status:
            # 修改自己订单状态
            print(request.POST.get('out_trade_no'), 'my_out_trade_no')
            # print('返回的订单号是:{}'.format(request.POST.get('')))
            pass
        return HttpResponse('POST返回')

    else:
        # params = request.GET
        print('支付宝回调,get请求============')
        params = request.GET.copy()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('GET验证', status)
        if status:
            order_id = request.GET.get('out_trade_no')
            print(order_id,'order_id')
            order_obj = Order.objects.get(order_id=order_id)
            pay_status = OrderStatusAndBillStatus.objects.get(status_content='买家已付款')
            order_obj.bill_status = pay_status
            order_obj.save()
        return HttpResponse('支付成功')
