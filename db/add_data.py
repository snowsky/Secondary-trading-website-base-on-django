import os
import sys
BASE_DIR = r'/home/cqh/python_project_dir/salt_fish/'
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salt_fish.settings") # 项目名如果直接包含django,好像会报错,使用其他的名称正常
# 2. 启动Django
import django
import pymysql
pymysql.install_as_MySQLdb()
django.setup()
from good.models import Good, GoodStatusAndSellMethod
from user.models import User
from good.models import GoodStatusAndSellMethod, Category
from order.models import OrderStatusAndBillStatus, Order

# 定义商品的状态表
# good_status_sell_method_list = [
#     (1, '待审核'),
#     (2,	'已发布'),
#     (3, '交易中'),
#     (4, '交易完成'),
#     (5,	'审核失败'),
#     (6, '当面交易'),
#     (7,	'快递'),
#     (8, '不限交易方式'),
# ]
#
# # 添加商品状态表
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
#
#
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

# User.objects.create(telephone='13381580718', username='cqh123', password='abc123')


# 商品信息的发布
# for i in range(50):
#     """
#     title = models.CharField(max_length=128, verbose_name='商品标题')
#     content = models.TextField(verbose_name='商品详情')
#     # original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
#     original_price = models.FloatField(verbose_name='原价')
#     current_price = models.FloatField(verbose_name='现价')
#     # current_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='现价')
#     # sell_method = models.SmallIntegerField(choices=sell_method_choices, default=2, verbose_name='交易方式')
#     # good_status = models.SmallIntegerField(choices=good_status_choices, default=0, verbose_name='商品状态')
#     sell_method = models.ForeignKey(to='GoodStatusAndSellMethod', related_name='good_sell_method', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='交易方式')
#     good_status = models.ForeignKey(to='GoodStatusAndSellMethod', related_name='good_status', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='商品状态')
#     owner_user = models.ForeignKey(to='user.User', related_name='good_owner_user', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='商品发布者')
#     # 加一个关注商品的用户
#     star_users = models.ManyToManyField(to='user.User', related_name='good_star_users', db_constraint=False, verbose_name='关注用户')
#     category = models.ForeignKey(to='Category', null=True, on_delete=models.SET_NULL, db_constraint=False)
#     created_time = models.DateField(auto_n
#     """
#     title = '今日商品%s的发布的标题' % i
#     content = '今日商品{}发布的详情内容'.format(i)
#     original_price = 199
#     current_price = 19
#     sell_method = GoodStatusAndSellMethod.objects.get(pk=8)
#     good_status = GoodStatusAndSellMethod.objects.get(pk=2)
#     owner_user = User.objects.get(pk=1)
#     category = Category.objects.get(pk=2)
#     Good.objects.create(title=title, content=content, original_price=original_price,
#                         current_price=current_price, sell_method=sell_method, good_status=good_status,
#                         owner_user=owner_user, category=category)


# 订单信息的生成
"""
 order_id = models.CharField(max_length=128, unique=True, verbose_name='订单号')
    order_title = models.TextField(verbose_name='商品标题')
    buyer = models.ForeignKey(to='user.User', null=True, related_name='order_buyer', on_delete=models.SET_NULL, db_constraint=False, verbose_name='买家')
    seller = models.ForeignKey(to='user.User', null=True, related_name='order_seller', on_delete=models.SET_NULL, db_constraint=False, verbose_name='卖家')
    order_status = models.ForeignKey(to='OrderStatusAndBillStatus', related_name='order_status', null=True,  default=1, on_delete=models.SET_NULL, verbose_name='订单状态')
    bill_status = models.ForeignKey(to='OrderStatusAndBillStatus', related_name='bill_status', null=True, on_delete=models.SET_NULL, default=6, verbose_name='钱款状态')
    delivery_price = models.FloatField(verbose_name='运费')
    order_price = models.FloatField(verbose_name='订单金额')
    delivery = models.ForeignKey(to='Delivery', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='快递')
    created_time = models.DateField(auto_now_add=True, verbose_name='订单生成时间')
    good = models.ForeignKey(to='good.Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='订单对应商品')

    # 加一个字段,控制订单的是否被用户删除(生成时不用传值,默认为1,订单被用户删除改为0)
    buyer_is_show = models.IntegerField(default=1, verbose_name='买家是否显示订单')
    seller_is_show = models.IntegerField
"""
for i in range(50):
    order_id = i + 23
    order_title = '今日商品%s的发布的标题' % i
    buyer = User.objects.get(pk=2)
    seller = User.objects.get(pk=1)
    order_status = OrderStatusAndBillStatus.objects.get(pk=6)
    bill_status = OrderStatusAndBillStatus.objects.get(pk=1)
    order_price = 199
    good = Good.objects.get(pk=(i+12))
    Order.objects.create(order_title=order_title, buyer=buyer,seller=seller,
                         order_status=order_status, bill_status=bill_status,
                         order_price=order_price, good=good)