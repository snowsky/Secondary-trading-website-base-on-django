from celery import Celery

multi_cel = Celery('multi_cel',
                   broker='redis://127.0.0.1:6379/2',
                   backend='redis://127.0.0.1:6379/2',
                   # 包含进两个任务,一个发送校验的任务,一个校验结果的任务
                   include=[
                       'celery_verify_task.good_celery_task',
                       'celery_verify_task.celery_result_task'
                   ])
