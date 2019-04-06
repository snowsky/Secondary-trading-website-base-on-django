from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    """
    继承django的auth
    用户名
    密码
    邮箱
    手机号(短信验证码发送并验证)
    创建时间
    余额
    账户类型(超级账户负责管理和保证金交易),普通用户
    """
    id = models.AutoField(primary_key=True)
    type_choices = ((0, '普通用户'), (1, '超级用户'), (2, '冻结用户'))
    username = models.CharField(unique=True, max_length=64, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    # email = models.EmailField()
    telephone = models.BigIntegerField(unique=True, verbose_name='手机号')
    created_time = models.DateField(auto_now_add=True, verbose_name='用户注册日期')
    balance = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name='余额')
    user_type = models.IntegerField(choices=type_choices, default=2, verbose_name='用户类型')

    class Meta:
        verbose_name_plural = verbose_name = '用户'

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    """
    收件人姓名
    收件人手机
    收件人地址
    外键关联到用户表(一个用户对应多个地址,外键放在多的一方中)
    """
    receiver_name = models.CharField(max_length=64, verbose_name='收件人姓名')
    receiver_telephone = models.BigIntegerField(verbose_name='收件人手机')
    receiver_address = models.TextField(verbose_name='收件人地址')
    # 加一个外键关联用户表
    user = models.ForeignKey(to='User', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='用户')

    class Meta:
        verbose_name_plural = verbose_name = '用户收件地址'


class IdCard(models.Model):
    """
    身份证号
    身份证照片
    验证状态
    """
    id_card_status_choices = ((0, '待审核'), (1, '审核通过'), (2, '审核失败'))
    id_card_number = models.BigIntegerField(verbose_name='身份证号')
    id_card_pic = models.ImageField(verbose_name='身份证图片')
    # 加一个外键关联用户表
    user = models.ForeignKey(to='User', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='用户')

    class Meta:
        verbose_name_plural = verbose_name = '用户身份证验证'


class Good(models.Model):
    """
    商品标题
    商品详情
    商品原价
    商品现价
    商品交易方式(同城当面,快递,都可以)
    商品状态(已发布,交易中,交易完成)
    评价(关联评价表的商品)
    关注商品的用户,多对多关联到用户表
    商品所属分类
    """
    SELL_FACE_TO_FACE = 0
    SELL_BY_DELIVERY = 1
    SELL_ALL_OK = 2
    sell_method_choices = ((SELL_FACE_TO_FACE, '同城当面交易'), (SELL_BY_DELIVERY, '快递'), (SELL_ALL_OK, '不限交易方式'))
    title = models.CharField(max_length=128, verbose_name='商品标题')
    content = models.TextField(verbose_name='商品详情')
    original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
    current_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='现价')
    sell_method = models.PositiveIntegerField(choices=sell_method_choices, default=2, verbose_name='交易方式')
    owner_user = models.ForeignKey(to='User', related_name='good_owner_user', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='商品发布者')
    # 加一个关注商品的用户
    star_users = models.ManyToManyField(to='User', related_name='good_star_users', db_constraint=False, verbose_name='关注用户')
    category = models.ForeignKey(to='Category', null=True, on_delete=models.SET_NULL, db_constraint=False)

    class Meta:
        verbose_name_plural = verbose_name = '商品'


class Category(models.Model):
    name = models.CharField(max_length=64)
    create_user = models.OneToOneField(to='User', null=True, on_delete=models.SET_NULL, db_constraint=False)
    created_time = models.DateField(auto_now_add=True, null=True)


class ChatRecord(models.Model):
    """
    id
    商品id
    发送者id(外键关联user表)一个用户会有多个聊天记录,一对多,把外键设置在多的一方
    接收者id(外键关联user表)一个用户会有多个聊天记录,一对多,把外键设置在多的一方

    可选功能:(接受者删除聊天记录标识:0不删除,1删除
            发送者删除聊天记录标识:0不删除,1删除)
    消息详情内容
    消息时间
    """
    good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='聊天相关商品')
    sender = models.OneToOneField(to='User', related_name='chat_sender', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='发送方')
    receiver = models.OneToOneField(to='User', related_name='chat_receiver', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='接收方')
    created_time = models.DateField(auto_now_add=True, verbose_name='聊天时间')
    content = models.TextField(verbose_name='聊天内容')

    class Meta:
        verbose_name_plural = verbose_name = '聊天记录'


class GoodPictures(models.Model):
    """
    id
    商品图标路径
    是否是主图
    一个商品对应多个图片,在多的一方图片类中加外键,关联商品类
    """
    image = models.ImageField(verbose_name='图片')
    is_main_pic = models.BooleanField(default=0, verbose_name='是否是主图')
    # 加外键关联商品
    good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='对应商品')

    class Meta:
        verbose_name_plural = verbose_name = '商品图片'


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
    bill_status_choices = ((0, '买家已付款'), (1, '卖家已收款'), (3, '买家已申请退款'), (4, '卖家已退款'))
    order_status_choices = ((0, '卖家未发货'), (1, '卖家已发货'), (2, '买家已收货'), (3, '买家已退货'), (4, '卖家已收货'))
    buyer = models.ForeignKey(to='User', related_name='order_buyer', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='买家')
    seller = models.ForeignKey(to='User', related_name='order_seller', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='卖家')
    order_status = models.PositiveIntegerField(choices=order_status_choices, default=0, verbose_name='订单状态')
    bill_status = models.IntegerField(choices=bill_status_choices, default=0, verbose_name='钱款状态')
    amount = models.PositiveIntegerField(null=True, verbose_name='交易金额')
    delicery_account = models.PositiveIntegerField(verbose_name='运费')
    delivery = models.ForeignKey(to='Delivery', null=True, on_delete=models.SET_NULL, db_constraint=False)
    created_time = models.DateField(auto_now_add=True, verbose_name='订单生成时间')

    class Meta:
        verbose_name_plural = verbose_name = '订单详情'


class Delivery(models.Model):
    """
    订单号
    运输公司
    """
    delivery_id = models.BigIntegerField()
    delivery_company = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = verbose_name = '运单'


class Comment(models.Model):
    """
    id
    评价用户
    父评价
    评价内容
    一件商品会有多条评论留言,在多的一方评价表中设置外键,关联商品表
    """
    user = models.OneToOneField(to='User', verbose_name='评论用户')
    parent = models.OneToOneField(to='self', verbose_name='父评价')
    content = models.TextField()
    # ForeignKey 关联到商品
    good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='评论商品')

    class Meta:
        verbose_name_plural = verbose_name = '商品评论详情'