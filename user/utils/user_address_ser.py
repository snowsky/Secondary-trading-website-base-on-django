from rest_framework import serializers
from user.models import UserAddress
from user.models import User
from rest_framework.exceptions import ValidationError
import re


class UserAddressSerializer(serializers.Serializer):
    receiver_name = serializers.CharField(max_length=64)
    receiver_telephone = serializers.CharField(max_length=64)
    receiver_address = serializers.CharField(max_length=1024)
    # 加一个外键关联用户表
    user = serializers.CharField()

    def validate_receiver_telephone(self, value):
        telephone_reg = r'^1[3|4|5|7|8][0-9]{9}$'

        if not re.match(telephone_reg, value):
            raise ValidationError('手机号格式错误')
        return value

    def create(self, validated_data):
        """
        receiver_name = models.CharField(max_length=64, verbose_name='收件人姓名')
    receiver_telephone = models.BigIntegerField(verbose_name='收件人手机')
    receiver_address = models.TextField(verbose_name='收件人地址')
    # 加一个外键关联用户表
    user
        :param validated_data:
        :return:
        """
        user_id = validated_data['user']
        validated_data['user'] = User.objects.get(pk=user_id)

        return UserAddress.objects.create(**validated_data)