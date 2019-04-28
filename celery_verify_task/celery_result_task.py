# 异步查询celery执行结果的类
from celery.result import AsyncResult
import redis
# from .good_celery_task import cel
from user.utils.my_redis_tool import POOL
from good.models import Good, GoodStatusAndSellMethod
from user.models import User
from django.db import transaction
import celery

# 单celery任务的设置
# # 消息中间件
# broker = 'redis://127.0.0.1:6379/2'
#
# # 结果存储
# backend = 'redis://127.0.0.1:6379/2'
#
# result_cel = celery.Celery('result_cel', broker=broker, backend=backend)

# 多任务celery设置的导入

from celery_verify_task.celery import multi_cel

# 传来的check_id是good_商品id的格式
@multi_cel.task
def check_celery_result_then_change_good_status(good_id):
    # 建立redis连接
    print('校验结果的函数开始执行')
    conn = redis.Redis(connection_pool=POOL)
    check_id = 'good_celery_{}'.format(good_id)
    res_id = conn.get(check_id)
    if not res_id:
        check_celery_result_then_change_good_status(good_id)
    res_id = str(res_id, encoding='utf-8')
    # print(str(res_id))
    # print(res_id)
    # print('任务的id:{}.++++++++++++++++++++++++++++++++++++++++++'.format(res_id))
    async = AsyncResult(id=res_id, app=multi_cel)
    # print('async.successful()', async.successful())
    if async.successful():
        result = async.get()
        print('result+++++++++++++++++++++++++:', result)
        print('type(result)', type(result))
        # 商品的内容和图片校验为True时,表示该商品信息非法,修改原商品状态为未审核通过
        if result:
            fail_good_status = GoodStatusAndSellMethod.objects.get(status_content='审核失败')
            good_obj = Good.objects.get(pk=good_id)
            # 商品状态修改为审核失败
            good_obj.good_status = fail_good_status
            # 将用户状态变为冻结状态,无法再发布商品
            user_obj = User.objects.get(pk=good_obj.owner_user_id)
            user_obj.user_type = 2
            # 商品和用户状态修改后的保存
            with transaction.atomic():
                good_obj.save()
                user_obj.save()
                print('商品id:{},含有敏感文字或图片,审核不通过,状态已修改为审核失败'.format(good_id))
                conn.delete(check_id)
                return
        else:
            # 将商品状态修改为已发布
            success_good_status = GoodStatusAndSellMethod.objects.get(status_content='已发布')
            good_obj = Good.objects.get(pk=good_id)
            good_obj.good_status = success_good_status
            good_obj.save()

            print('商品id:{},审核通过,状态已修改为已发布')
            conn.delete(check_id)
        # 将redis中保存的任务id的值给删除

        return
    elif async.failed():
        print('商品id:{}的校验任务执行失败'.format(good_id))
        return
    else:
        print('当前异步校验商品的任务状态是:{}..继续等待校验任务完成',async.status)
        import time
        time.sleep(5)
        check_celery_result_then_change_good_status(good_id)
        print('校验函数开始下一次循环')

    print('校验结果的函数执行完成')


