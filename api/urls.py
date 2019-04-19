from django.conf.urls import url
from api.views import api_good_views
from api.views import api_order_views

urlpatterns = [
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
]
