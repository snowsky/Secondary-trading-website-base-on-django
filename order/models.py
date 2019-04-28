from django.db import models

# Create your models here.


class Order(models.Model):
    """
    订单号id
    买家id(外键关联user表)
    卖家id(外键关联user表)
    金钱往来记录(关联金钱往来记录)
    商品id
    订单状态:付款未发货,已发货,已收货
    订单金额
    订单创建时间
    """

    order_id = models.CharField(max_length=128, unique=True, verbose_name='订单号')
    order_title = models.TextField(verbose_name='商品标题')
    buyer = models.ForeignKey(to='user.User', null=True, related_name='order_buyer', on_delete=models.SET_NULL, db_constraint=False, verbose_name='买家')
    seller = models.ForeignKey(to='user.User', null=True, related_name='order_seller', on_delete=models.SET_NULL, db_constraint=False, verbose_name='卖家')
    order_status = models.ForeignKey(to='OrderStatusAndBillStatus', related_name='order_status', null=True,  default=6, on_delete=models.SET_NULL, verbose_name='订单状态')
    bill_status = models.ForeignKey(to='OrderStatusAndBillStatus', related_name='bill_status', null=True, on_delete=models.SET_NULL, default=1, verbose_name='钱款状态')
    delivery_price = models.FloatField(default=0, verbose_name='运费')
    drawback_delivery_price = models.FloatField(null=True, verbose_name='退货运费')
    order_price = models.FloatField(verbose_name='订单金额')
    delivery = models.ForeignKey(to='Delivery', related_name='delivery', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='快递')
    drawback_delivery = models.ForeignKey(to='Delivery', related_name='drawback_delivery', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='退货快递')
    created_time = models.DateField(auto_now_add=True, verbose_name='订单生成时间')
    good = models.ForeignKey(to='good.Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='订单对应商品')

    # 加一个字段,控制订单的是否被用户删除(生成时不用传值,默认为1,订单被用户删除改为0)
    buyer_is_show = models.IntegerField(default=1, verbose_name='买家是否显示订单')
    seller_is_show = models.IntegerField(default=1, verbose_name='买家是否显示订单')

    # 加一个字段,外键关联到收货地址
    buyer_address = models.ForeignKey(to='user.UserAddress', related_name='order_buyer_address', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='订单收货人信息')
    seller_address = models.ForeignKey(to='user.UserAddress', related_name='order_seller_address', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='订单发货人信息')

    class Meta:
        verbose_name_plural = verbose_name = '订单详情'


class OrderStatusAndBillStatus(models.Model):
    """
    ((0, '待买家付款'), (1, '买家已付款'), (2, '卖家已收款'), (3, '买家已申请退款'), (4, '卖家已退款'),
    (5, '卖家未发货'), (6, '卖家已发货'), (7, '买家已收货'), (8, '买家已退货'), (9, '卖家已收货'))
    """
    status_number = models.SmallIntegerField(unique=True, verbose_name='状态编号')
    status_content = models.CharField(unique=True, max_length=128, verbose_name='状态内容')

    class Meta:
        verbose_name_plural = verbose_name = '订单状态和钱款状态'


class Delivery(models.Model):
    """
    运单号
    运输公司
    """
    # delivery_id = models.BigIntegerField(verbose_name='订单号')
    delivery_company = models.CharField(null=True, max_length=64, verbose_name='快递公司')
    receiver_address = models.TextField(null=True, verbose_name='收货地址')
    receiver_name = models.CharField(null=True, max_length=128, verbose_name='收货人姓名')
    receiver_telephone = models.CharField(null=True, max_length=128, verbose_name='收货人手机')

    sender_address = models.TextField(null=True, verbose_name='发货人地址')
    sender_telephone = models.CharField(null=True, max_length=128, verbose_name='发货人手机')
    sender_name = models.TextField(null=True, verbose_name='发货人姓名')

    class Meta:
        verbose_name_plural = verbose_name = '运单'