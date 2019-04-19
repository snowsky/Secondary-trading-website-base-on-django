import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salt_fish.settings") # 项目名如果直接包含django,好像会报错,使用其他的名称正常
# 2. 启动Django
import django
import pymysql
pymysql.install_as_MySQLdb()
django.setup()
from user.models import User
from good.models import GoodStatusAndSellMethod, Category
from order.models import OrderStatusAndBillStatus

# 定义商品的状态表
good_status_sell_method_list = [
    (1, '待审核'),
    (2,	'已发布'),
    (3, '交易中'),
    (4, '交易完成'),
    (5,	'审核失败'),
    (6, '当面交易'),
    (7,	'快递'),
    (8, '不限交易方式'),
]

# 添加商品状态表
# for item in good_status_sell_method_list:
#     GoodStatusAndSellMethod.objects.create(status_number=item[0], status_content=item[1])
#
# # 定义商品的分类信息
#
# # 商品分类
# categories = [
#     (1,	'手机'),
#     (2,	'数码'),
#     (3,	'租房'),
#     (4,	'服装'),
#     (5,	'居家'),
#     (6, '美妆'),
#     (7,	'运动'),
#     (8,	'家电'),
#     (9,	'玩具乐器')
# ]
#
# for item in categories:
#     Category.objects.create(category_id=item[0], name=item[1])


# order_status_bill_status_list = [
#     (1, '待买家付款'),
#     (2, '买家已付款'),
#     (3, '卖家已收款'),
#     (4, '买家已申请退款'),
#     (5, '卖家已退款'),
#     (6, '卖家未发货'),
#     (7, '卖家已发货'),
#     (8, '买家已收货'),
#     (9, '买家已退货'),
#     (10, '卖家已收货')
# ]
#
# for item in order_status_bill_status_list:
#     OrderStatusAndBillStatus.objects.create(status_number=item[0], status_content=item[1])

User.objects.create(telephone='13381580718', username='cqh123', password='abc123')