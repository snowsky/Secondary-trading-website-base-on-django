# 单文件测试函数时需要配置的django设置
# import os
# import sys
# BASE_DIR = r'/home/cqh/python_project_dir/salt_fish/'
# sys.path.append(BASE_DIR)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salt_fish.settings") # 项目名如果直接包含django,好像会报错,使用其他的名称正常
# # 2. 启动Django
# import django
# import pymysql
# pymysql.install_as_MySQLdb()
# django.setup()
import redis
from user.utils.my_redis_tool import POOL
from .good_celery_task import good_verify
from .celery_result_task import check_celery_result_then_change_good_status


# 添加任务的时候传参商品id,并且开始一个定时任务,检查celery任务的状态
def add_good_verify_celery_task(good_id):
    conn = redis.Redis(connection_pool=POOL)
    res = good_verify.delay(good_id)
    res_id = res.id
    # 要在redis中存储数据,name=good_商品id,value=celery任务id
    conn.set('good_celery_{}'.format(good_id), res_id)
    # print(res_id)
    check_celery_result_then_change_good_status.delay(good_id)
    return res_id
