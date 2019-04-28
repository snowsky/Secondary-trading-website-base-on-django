# from rest_framework.views import APIView
from celery_verify_task.good_celery_task import good_verify
from django.shortcuts import HttpResponse
from celery_verify_task.content_verify import ArticleSafe
from good.models import Good, GoodPictures
from celery_verify_task.pic_verify import PicVerify


# 没有验证,纯测试接口
def verify_good_by_id(request, good_id):
    if request.method == 'GET':
        a_tool = ArticleSafe()
        good_obj = Good.objects.get(pk=good_id)
        pure_text = a_tool.pure_article_without_punc(good_obj.title)

        title_status = a_tool.check_article_safe(pure_text, a_tool.safe_dict_content)

        pure_text = a_tool.pure_article_without_punc(good_obj.content)

        content_status = a_tool.check_article_safe(pure_text, a_tool.safe_dict_content)

        final_status = title_status or content_status

        if final_status:
            return HttpResponse('商品标题或文字中含有敏感词')

        else:
            return HttpResponse('商品信息正常')


def verify_pic_by_id(request, pic_id):
    if request.method == 'GET':
        pic_obj = GoodPictures.objects.get(pk=pic_id)
        pic_ver_obj = PicVerify(pic_obj.image_path)
        pic_ver_obj.resize()
        res = pic_ver_obj.parse()
        image_data = res.showSkinRegions()
        return HttpResponse(image_data, 'image/jpg')