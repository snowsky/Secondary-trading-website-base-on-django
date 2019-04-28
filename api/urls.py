from django.conf.urls import url
from api.views import api_good_views
from api.views import api_order_views
from api.views import api_user_views
from api.views import api_verify_views

urlpatterns = [
    # 验证文字内容的接口,传商品id
    url(r'^verify/good/(?P<good_id>\d+)/$', api_verify_views.verify_good_by_id),

    # 校验图片的接口,传pic_id
    url(r'^verify/pic/(?P<pic_id>\d+)/$', api_verify_views.verify_pic_by_id),

    # 买家退货发货成功后,卖家收货退款给买家的操作的接口
    url(r'^seller_receive_drawback/(?P<order_id>\d+)/$', api_order_views.SellerReceiveDeliveryDrawback.as_view()),

    # 买家申请退款成功后,买家继续进行退货发货操作的接口
    url(r'^buyer_send_drawback/(?P<order_id>\d+)/$', api_order_views.BuyerSendDrawbackDelivery.as_view()),

    # 买家收货后,买家申请退款的接口
    url(r'^buyer_motion_drawback/(?P<order_id>\d+)/$', api_order_views.BuyerMotionDrawback.as_view()),

    # 卖家已发货后,买家确认收货的接口
    url(r'^buyer_receive_delivery/(?P<order_id>\d+)/$', api_order_views.BuyerReceiveDelivery.as_view()),

    # 买家已付款后订单的卖家发货接口
    url(r'^seller_send_delivery/(?P<order_id>\d+)/$', api_order_views.SellerSendDelivery.as_view()),

    # 商品发布的信息的获取和上传
    url(r'^good_release/$', api_good_views.GoodRelease.as_view(), name='good_release'),
    # 发布后的商品的查询及修改删除
    url(r'^good_edit/(?P<good_id>\d*)/$', api_good_views.GoodEdit.as_view(), name='good_edit'),
    # 其他用户获取别人发布的商品的信息
    url(r'^good/(?P<good_id>\d+)/$', api_good_views.GetGoodById.as_view(), name='get_good_by_id'),
    # 用于单独获取图片链接的二进制文件数据
    url(r'^pic/(?P<pic_id>\d+)/$', api_good_views.GetPicById.as_view(), name='get_pic_by_id'),



    # 用户购买商品,接受信息并生成订单信息
    # 携带商品id,当前用户可从request中获取到,
    url(r'^buy/(?P<good_id>\d+)/$', api_order_views.BuyByGoodId.as_view(), name='buy_good_by_id'),
    # 返回当前订单和钱款可用的所有状态
    url(r'^all_order_bill_status/$', api_order_views.GetOrderStatusAndBillStatus.as_view(), name='all_order_bill_status'),
    # 删除订单(实际只是修改订单状态让其不显示)
    url(r'^edit_order/(?P<order_id>\d+)/$', api_order_views.EditOrder.as_view(), name='edit_order'),
    # 查询已买商品的订单的接口
    url(r'^buy_order/$', api_order_views.GetBuyOrder.as_view(), name='get_buy_order'),
    # 查询已卖商品的订单的接口
    url(r'^sell_order/$', api_order_views.GetSellOrder.as_view(), name='get_sell_order'),


    # 查询已生成订单的接口,返回订单的当前所有信息

    # 为用户AddAddress 添加用户收货地址的接口
    url(r'^add_address/$', api_user_views.AddAddress.as_view(), name='add_address'),
]
