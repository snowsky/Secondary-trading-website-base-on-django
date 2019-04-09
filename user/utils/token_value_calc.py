# 为token的值加密并验证token的类
import hashlib


# 生成token的函数做成类
class CheckUserToken:
    def __init__(self):
        self.user_md5 = hashlib.md5()

    def get_token_key(self, telephone):
        self.user_md5.update(telephone.encode('utf-8'))
        token_key = self.user_md5.hexdigest()
        return token_key

    def get_token_str(self, telephone):
        # 生成token值
        self.user_md5.update(telephone.encode('utf-8'))
        # token的key,是对手机号md5的加密
        token_key = self.user_md5.hexdigest()
        # print('md5', token_key)
        # 生成token对应数据的加密结果
        # token的值是对手机的md5的加密之后再加密
        token_value = self.get_token_value(token_key)

        token_str = '{}|{}'.format(str(token_key), str(token_value))
        # token_str = str(token_key) + '|' + str(token_value)
        return token_str

    def get_token_value(self, token_key):
        liss = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        mima = "QWERTYUIOPASDFGHJKLZXCVBNM "
        change_token = token_key.upper()
        temp = ""
        for i in range(5):
            for j in change_token:
                n = liss.find(j)
                temp += mima[n]
            # print(temp)
            change_token = temp
            temp = ""
        # print(change_token)
        change_token = ''.join(change_token.split())
        return change_token

    # 传客户端带来的校验对应的数据
    def check_token(self, token_str):
        token_key = token_str.split('|')[0]
        token_value = token_str.split('|')[-1]
        if token_value == str(self.get_token_value(token_key)):
            return True
        else:
            return False
