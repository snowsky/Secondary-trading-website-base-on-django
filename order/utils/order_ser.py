from datetime import datetime
from rest_framework import serializers
from good.models import Good
from order.models import OrderStatusAndBillStatus, Order
from user.models import User


class SaveOrderSerializer(serializers.Serializer):
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

    """
    order_id = serializers.CharField(required=False)
    order_title = serializers.CharField(min_length=6, error_messages={'min_length': '标题至少6个字'})
    buyer = serializers.IntegerField()
    seller = serializers.IntegerField()
    order_status = serializers.IntegerField()
    bill_status = serializers.IntegerField()
    delivery_price = serializers.FloatField(min_value=0.00, error_messages={'min_value': '运费应为正数'})
    order_price = serializers.FloatField(min_value=0.01, error_messages={'min_value': '订单价格应为正数'})
    delivery = serializers.IntegerField(required=False)
    created_time = serializers.DateField(required=False)

    # 控制订单是否显示(有无被用户删除),生成订单不用传值,默认为1显示,删除时更新为0
    is_show = serializers.IntegerField(required=False)

    good = serializers.IntegerField()

    def create(self, validated_data):

        good_obj = Good.objects.get(pk=validated_data['good'])
        # good_sell_status = GoodStatusAndSellMethod.objects.get(status_content='交易中')
        # if good_obj.good_status != good_sell_status:
        #     raise ValidationError('该商品已无法购买')
        validated_data['good'] = good_obj
        import uuid
        t = datetime.now()
        ft = t.strftime('%Y%m%d%H%M%S')
        # print('ft', ft)
        buyer_id = validated_data['buyer']
        validated_data['buyer'] = User.objects.get(pk=buyer_id)
        seller_id = validated_data['seller']
        validated_data['seller'] = User.objects.get(pk=seller_id)

        # 订单号用uuid+商品标题的md5值+当前时间
        order_id = '{}{}{}'.format(uuid.uuid4(), buyer_id, ft)
        order_status_id = validated_data['order_status']
        # print(order_status_id)
        validated_data['order_status'] = OrderStatusAndBillStatus.objects.get(pk=order_status_id)
        # validated_data['order_status'] = order_status
        validated_data['bill_status'] = OrderStatusAndBillStatus.objects.get(pk=validated_data['bill_status'])


        print({**validated_data})
        order_obj = Order.objects.create(order_id=order_id, **validated_data)
        print(type(order_obj))
        return order_obj


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'