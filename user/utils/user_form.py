import re

from django import forms
from django.core.exceptions import ValidationError


# 自定义一个校验要使用的类
class LoginCheckForm(forms.Form):
    telephone = forms.CharField(min_length=11, max_length=11, error_messages={'min_length': '手机号应为11位',
                                                                              'max_length': '用户名应为11位'})
    passwd = forms.CharField(min_length=6, max_length=20, error_messages={'min_length': '密码至少6位',
                                                                          'max_length': '密码至多20位'})

    def clean_telephone(self):
        telephone_reg = r'^1[3|4|5|7|8][0-9]{9}$'
        telephone = self.cleaned_data.get('telephone')  # type:str
        if not re.match(telephone_reg, telephone):
            raise ValidationError('手机号格式错误')
        return telephone


class RegisterCheckForm(forms.Form):
    telephone = forms.CharField(min_length=11, max_length=11, error_messages={'min_length': '手机号至少11位',
                                                                              'max_length': '手机号至多11位'})
    passwd = forms.CharField(min_length=6, max_length=20, error_messages={'min_length': '密码至少6位',
                                                                          'max_length': '密码至多20位'})
    confirm_passwd = forms.CharField(min_length=6, max_length=20, error_messages={'min_length': '密码至少6位',
                                                                                  'max_length': '密码至多20位'})
    code = forms.CharField(min_length=4, max_length=4, error_messages={'min_length': '验证码至少4位',
                                                                       'max_length': '验证码至多4位'})
    username = forms.CharField(min_length=6, max_length=20, error_messages={'min_length': '用户名至少6位',
                                                                            'max_length': '用户名至多20位'})

    def clean_telephone(self):
        telephone_reg = r'^1[3|4|5|7|8][0-9]{9}$'
        telephone = self.cleaned_data.get('telephone')
        if not re.match(telephone_reg, telephone):
            raise ValidationError('手机号格式错误')
        return telephone

    def clean(self):
        passwd = self.cleaned_data.get('passwd')
        confirm_passwd = self.cleaned_data.get('confirm_passwd')
        if passwd != confirm_passwd:
            raise ValidationError('两次密码不一致')
        return self.cleaned_data