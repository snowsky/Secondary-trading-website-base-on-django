# 公共响应
class CommonResponse:
    def __init__(self):
        # 100正常返回,不携带数据
        # 200正常返回,携带数据
        self.status = 100
        self.msg = None
        self.data = None

    def get_dic(self):
        return self.__dict__