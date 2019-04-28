from rest_framework import serializers
from good.models import Good, GoodPictures
from rest_framework.exceptions import ValidationError
from good.models import Good, Category, GoodStatusAndSellMethod
from user.models import User


class GoodAndPictureSerializers(serializers.Serializer):
    '''
    SELL_FACE_TO_FACE = 0
    SELL_BY_DELIVERY = 1
    SELL_ALL_OK = 2
    sell_method_choices = ((SELL_FACE_TO_FACE, '同城当面交易'), (SELL_BY_DELIVERY, '快递'), (SELL_ALL_OK, '不限交易方式'))
    good_status_choices = ((0, '在售'), (1, '已售出'))
    title = models.CharField(max_length=128, verbose_name='商品标题')
    content = models.TextField(verbose_name='商品详情')
    original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
    current_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='现价')
    sell_method = models.SmallIntegerField(choices=sell_method_choices, default=2, verbose_name='交易方式')
    good_status = models.SmallIntegerField(choices=good_status_choices, default=0, verbose_name='商品状态')
    owner_user = models.ForeignKey(to='user.User', related_name='good_owner_user', null=True, on_delete=models.SET_NULL,
                                   db_constraint=False, verbose_name='商品发布者')
    # 加一个关注商品的用户
    star_users = models.ManyToManyField(to='user.User', related_name='good_star_users', db_constraint=False,
                                        verbose_name='关注用户')
    category = models.ForeignKey(to='Category', null=True, on_delete=models.SET_NULL, db_constraint=False)
    image = models.ImageField(verbose_name='图片')
    is_main_pic = models.BooleanField(default=0, verbose_name='是否是主图')
    # 加外键关联商品
    good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='对应商品')
    '''
    # 商品good类的字段
    title = serializers.CharField(min_length=6, max_length=128,
                                  error_messages={'min_length': '标题至少6个字', 'max_length': '标题至多128个字'})
    content = serializers.CharField(min_length=10)
    original_price = serializers.FloatField(min_value=0.1, error_messages={'min_value': '价格不能为负数'})
    current_price = serializers.FloatField(min_value=0.1, error_messages={'min_value': '价格不能为负数'})
    sell_method = serializers.IntegerField()
    good_status = serializers.IntegerField(required=False)
    owner_user = serializers.IntegerField()
    category = serializers.IntegerField()
    # 商品照片Picture的字段

    # 写9个图片字段做序列化,但是除了第一张外,其他设置为required=False,并不一定要传
    img1 = serializers.FileField(required=False)
    img2 = serializers.FileField(required=False)
    img3 = serializers.FileField(required=False)
    img4 = serializers.FileField(required=False)
    img5 = serializers.FileField(required=False)
    img6 = serializers.FileField(required=False)
    img7 = serializers.FileField(required=False)
    img8 = serializers.FileField(required=False)
    img9 = serializers.FileField(required=False)

    # method = serializers.ChoiceField(choices=((0, '发布'), (1, '更新')))

    # 该字段存成列表形式,用来确认前端到底传了几张图片来
    image = serializers.ListField()

    main_img = serializers.CharField()

    def validate(self, attrs):
        if attrs['original_price'] < attrs['current_price']:
            raise ValidationError('现价不能高于原价')
        return attrs

    def create(self, validated_data):
        # 偷梁换柱,把传来的外键的id转换成对象,再替换掉validated_data中对应的数据
        # 这样再保存数据就不会有问题
        print(validated_data)
        user_id = validated_data['owner_user']
        user = User.objects.get(pk=user_id)
        validated_data['owner_user'] = user

        # 转换交易方式将id转成对象
        sell_method_id = validated_data['sell_method']
        validated_data['sell_method'] = GoodStatusAndSellMethod.objects.get(pk=sell_method_id)
        # good_status_id = validated_data['good_status']
        # validated_data['good_status'] = GoodStatusAndSellMethod.objects.get(pk=good_status_id)

        # 转换分类标签
        category_id = validated_data['category']
        category = Category.objects.get(pk=category_id)
        validated_data['category'] = category

        # 去除图片类中的字段
        validated_data.pop('image')
        validated_data.pop('main_img')
        # print(validated_data)

        return Good.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user_id = validated_data['owner_user']
        user = User.objects.get(pk=user_id)
        validated_data['owner_user'] = user

        # 转换分类标签
        category_id = validated_data['category']
        category = Category.objects.get(pk=category_id)
        validated_data['category'] = category

        # 去除图片类中的字段
        validated_data.pop('image')
        validated_data.pop('main_img')
        # print(validated_data)

        return instance.update(**validated_data)


class GoodSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Good

# class GoodSerializers(serializers.ModelSerializer):
#     '''
#     SELL_FACE_TO_FACE = 0
#     SELL_BY_DELIVERY = 1
#     SELL_ALL_OK = 2
#     sell_method_choices = ((SELL_FACE_TO_FACE, '同城当面交易'), (SELL_BY_DELIVERY, '快递'), (SELL_ALL_OK, '不限交易方式'))
#     good_status_choices = ((0, '在售'), (1, '已售出'))
#     title = models.CharField(max_length=128, verbose_name='商品标题')
#     content = models.TextField(verbose_name='商品详情')
#     original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
#     current_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='现价')
#     sell_method = models.SmallIntegerField(choices=sell_method_choices, default=2, verbose_name='交易方式')
#     good_status = models.SmallIntegerField(choices=good_status_choices, default=0, verbose_name='商品状态')
#     owner_user = models.ForeignKey(to='user.User', related_name='good_owner_user', null=True, on_delete=models.SET_NULL,
#                                    db_constraint=False, verbose_name='商品发布者')
#     # 加一个关注商品的用户
#     star_users = models.ManyToManyField(to='user.User', related_name='good_star_users', db_constraint=False,
#                                         verbose_name='关注用户')
#     category = models.ForeignKey(to='Category', on_delete=models.SET_NULL, db_constraint=False)
#
#
#     image = models.ImageField(verbose_name='图片')
#     is_main_pic = models.BooleanField(default=0, verbose_name='是否是主图')
#     # 加外键关联商品
#     good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='对应商品')
#
#     class Meta:
#         verbose_name_plural = verbose_name = '商品图片'
#
#     def __str__(self):
#         return self.image
#     '''
#     # 商品good类的字段
#     class Meta:
#         fields = '__all__'
#         model = Good
#
#     # def valid_title(self, value):
#     #     if len(value) <= 0 or len(value) > 128:
#     #         raise ValidationError('标题长度错误')
#     #     return value
#     #
#     # def valid_content(self, value):
#     #     if not value:
#     #         raise ValidationError('商品内容不能为空')
#     #     return value
#     #
#     # def valid_original_price(self, value):
#     #     try:
#     #         number = float(value)
#     #     except ValueError:
#     #         print("not a number")
#     #         raise ValidationError('价格格式错误')
#     #     return value
#     #
#     # def valid_current_price(self, value):
#     #     try:
#     #         number = float(value)
#     #     except ValueError:
#     #         print("not a number")
#     #         raise ValidationError('价格格式错误')
#     #     return value
#     #
#     # def valid_sell_method(self, value):
#     #     if value not in [0, 1, 2]:
#     #         raise ValidationError('交易方式数据错误')
#     #     return value
#
#
# class GoodPictureSerializers(serializers.Serializer):
#     class Meta:
#         fields = '__all__'
#         model = GoodPictures
