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
    buyer = models.ForeignKey(to='user.User', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='买家')
    seller = models.ForeignKey(to='user.User', related_name='seller', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='卖家')
    order_status = models.ForeignKey(to='OrderStatusAndBillStatus', null=True, related_name='order_status', default=0, on_delete=models.SET_NULL, verbose_name='订单状态')
    bill_status = models.ForeignKey(to='OrderStatusAndBillStatus', related_name='bill_status', null=True, on_delete=models.SET_NULL, default=5, verbose_name='钱款状态')
    delivery_price = models.FloatField(verbose_name='运费')
    order_price = models.FloatField(verbose_name='订单金额')
    delivery = models.ForeignKey(to='Delivery', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='快递')
    created_time = models.DateField(auto_now_add=True, verbose_name='订单生成时间')
    good = models.ForeignKey(to='good.Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='订单对应商品')

    class Meta:
        verbose_name_plural = verbose_name = '订单详情'


class OrderStatusAndBillStatus(models.Model):
    """
    ((0, '买家已付款'), (1, '卖家已收款'), (3, '买家已申请退款'), (4, '卖家已退款'),
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
    delivery_id = models.BigIntegerField(verbose_name='订单号')
    delivery_company = models.CharField(max_length=64, verbose_name='快递公司')
    receive_address = models.TextField(verbose_name='收货地址')
    send_address = models.TextField(verbose_name='发货地址')

    class Meta:
        verbose_name_plural = verbose_name = '运单'