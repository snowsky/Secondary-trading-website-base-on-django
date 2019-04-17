from django.conf.urls import url
from api import views

urlpatterns = [
    # 商品发布的信息的获取和上传
    url(r'^good_release/$', views.GoodRelease.as_view(), name='good_release'),
    # 发布后的商品的查询及修改删除
    url(r'^good_edit/(?P<good_id>\d*)$', views.GoodEdit.as_view(), name='good_edit'),
    # 其他用户获取别人发布的商品的信息
    url(r'^good/(?P<good_id>\d+)/$', views.GetGoodById.as_view(), name='get_good_by_id'),
    # 用于单独获取图片链接的二进制文件数据
    url(r'^pic/(?P<pic_id>\d+)/$', views.GetPicById.as_view(), name='get_pic_by_id'),
    # 用户购买商品,接受信息并生成订单信息

    # 查询已生成订单的接口,返回订单的当前所有信息
]
