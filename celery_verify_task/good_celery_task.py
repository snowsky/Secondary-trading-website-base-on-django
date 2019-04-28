# 单文件测试函数时需要配置的django设置
import os
import sys
BASE_DIR = r'/home/cqh/python_project_dir/salt_fish/'
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salt_fish.settings") # 项目名如果直接包含django,好像会报错,使用其他的名称正常
# 2. 启动Django
import django
import pymysql
pymysql.install_as_MySQLdb()
django.setup()
# celery功能的开始
from good.models import Good, GoodPictures
from celery_verify_task.content_verify import ArticleSafe
from celery_verify_task.pic_verify import PicVerify
# 单任务时的celery配置
# # 消息中间件
# broker = 'redis://127.0.0.1:6379/2'
# # 结果存储
# backend = 'redis://127.0.0.1:6379/2'
# # 第一个参数,给celery命名
# cel = celery.Celery('good_verify', broker=broker, backend=backend)

# 多任务时,直接从配置的celery文件中导入celery任务的配置
from celery_verify_task.celery import multi_cel


@multi_cel.task
def good_verify(good_id):
    print('校验商品的任务开始')
    # 取出商品中的title和content的内容
    good_obj = Good.objects.get(pk=good_id)
    good_title = good_obj.title
    good_content = good_obj.content

    # 做文字内容的校验
    content_verify_tool = ArticleSafe()
    # 校验状态为title_flag,content_flag,True为正常,False为不正常
    title_flag = content_verify_tool.check_article_safe(content_verify_tool.pure_article_without_punc(good_title),
                                                        content_verify_tool.safe_dict_content)
    content_flag = content_verify_tool.check_article_safe(content_verify_tool.pure_article_without_punc(good_content),
                                                          content_verify_tool.safe_dict_content)
    # True为文字中有敏感词,需要屏蔽,False为没有敏感词,不需要操作
    good_flag = title_flag or content_flag

    # 取出商品对应的图片,发送到腾讯图片鉴别接口
    good_pic_list = GoodPictures.objects.filter(good=good_obj).all()
    for good_pic_item in good_pic_list:
        #  自己根据返回的json数据做判断,判断图片信息正确与否
        pic_ver_tool = PicVerify(good_pic_item.image_path)
        pic_result, verify_message = pic_ver_tool.verify_and_get_result_message()
        print(pic_result, verify_message)
        # 如果返回值是True,则是黄图,不需要再检查数据了
        if pic_result:
            final_flag = good_flag or pic_result
            print('校验商品结束')

            return final_flag
    print('校验商品结束')
    return good_flag


# 用来测试数据
if __name__ == '__main__':
    good_verify(3)