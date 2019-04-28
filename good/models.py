from django.db import models

# Create your models here.


class Good(models.Model):
    """
    商品标题
    商品详情
    商品原价
    商品现价
    商品交易方式(同城当面,快递,都可以)
    商品状态(已发布,交易中,交易完成)
    关注商品的用户,多对多关联到用户表
    商品所属分类
    """
    title = models.CharField(max_length=128, verbose_name='商品标题')
    content = models.TextField(verbose_name='商品详情')
    # original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
    original_price = models.FloatField(verbose_name='原价')
    current_price = models.FloatField(verbose_name='现价')
    # current_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='现价')
    # sell_method = models.SmallIntegerField(choices=sell_method_choices, default=2, verbose_name='交易方式')
    # good_status = models.SmallIntegerField(choices=good_status_choices, default=0, verbose_name='商品状态')
    sell_method = models.ForeignKey(to='GoodStatusAndSellMethod', related_name='good_sell_method', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='交易方式')
    good_status = models.ForeignKey(to='GoodStatusAndSellMethod', default=1, related_name='good_status', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='商品状态')
    owner_user = models.ForeignKey(to='user.User', related_name='good_owner_user', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='商品发布者')
    # 加一个关注商品的用户
    star_users = models.ManyToManyField(to='user.User', related_name='good_star_users', db_constraint=False, verbose_name='关注用户')
    category = models.ForeignKey(to='Category', null=True, on_delete=models.SET_NULL, db_constraint=False)
    created_time = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = verbose_name = '商品'

    def __str__(self):
        return self.title


class GoodStatusAndSellMethod(models.Model):
    # id = models.AutoField(primary_key=True)
    status_number = models.CharField(unique=True, max_length=50)
    status_content = models.CharField(unique=True, max_length=50)

    class Meta:
        # unique_together = ('status_number', 'status_content')
        verbose_name_plural = verbose_name = '商品及交易方式'

    def __str__(self):
        return self.status_content


class Category(models.Model):
    category_id = models.IntegerField(unique=True, null=True)
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        verbose_name_plural = verbose_name = '分类'

    def __str__(self):
        return self.name
    # create_user = models.OneToOneField(to='user.User', null=True, on_delete=models.SET_NULL, db_constraint=False)
    # created_time = models.DateField(auto_now_add=True, null=True)


class GoodPictures(models.Model):
    """
    id
    商品图标路径
    是否是主图
    一个商品对应多个图片,在多的一方图片类中加外键,关联商品类
    """
    image_status_choices = ((0, '非主图'), (1, '主图'))
    image_path = models.CharField(unique=True, max_length=254, null=True, verbose_name='图片存储路径')
    is_main_pic = models.SmallIntegerField(default=0, choices=image_status_choices, verbose_name='是否是主图')
    # 加外键关联商品
    good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='对应商品')

    class Meta:
        verbose_name_plural = verbose_name = '商品图片'

    def __str__(self):
        return self.__class__.__name__


class Comment(models.Model):
    """
    id
    评价用户
    父评价
    评价内容
    一件商品会有多条评论留言,在多的一方评价表中设置外键,关联商品表
    """
    user = models.OneToOneField(to='user.User', verbose_name='评论用户')
    parent = models.OneToOneField(to='self', verbose_name='父评价')
    content = models.TextField()
    # ForeignKey 关联到商品
    good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='评论商品')

    class Meta:
        verbose_name_plural = verbose_name = '商品评论详情'