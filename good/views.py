# import os
# import hashlib
# import time
# import json
# from django.shortcuts import render, HttpResponse
# from django.views import View
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from django.conf import settings
# from user.utils.common_response import CommonResponse
# from user.utils.user_drf_auth import UserTokenAuth
# from salt_fish.settings import GOOD_IMAGE_DIR
# from good.models import GoodPictures, Category, Good, GoodStatusAndSellMethod
# from good.utils.good_serilization import GoodAndPictureSerializers, GoodSerializers
#
# ip = '127.0.0.1'
#
# base_url = 'http://{}:8001/good/'.format(ip)
#
#
# class GetGoodById(APIView):
#     # 单商品详情页面
#     def get(self, request, pk):
#         return render(request, 'good_detail.html', locals())
#         # return render(request, 'good_detail.html', locals())
#
#
# class GoodRelease(APIView):
#     authentication_classes = [UserTokenAuth]
#
#     # 获取发布商品的页面(已完成) 把目前可发布的分类和交易方式,返回给前台
#     def get(self, request):
#         response = CommonResponse()
#         response.data = {}
#         # 校验完要取出当前用户的id,方便后续POST发数据回来的操作
#
#         # 返回所有交易方式
#         # get_sell_method_choices
#         try:
#             sell_method_and_status = GoodStatusAndSellMethod.objects.all()
#             # print(sell_method_choices)
#             response.data['sell_method_and_status'] = {}
#             response.data['category'] = {}
#             for s in sell_method_and_status:
#                 response.data['sell_method_and_status'][s.id] = s.status_content
#             # 返回商品的所有分类,供用户在前台选择发布到哪个分类下
#             category_list = Category.objects.all()
#
#             for c in category_list:
#                 response.data['category'][c.id] = c.name
#
#             print(response.data)
#
#             response.status = 200
#             response.msg = '商品分类与交易方式获取成功'
#         except Exception as e:
#             print(e)
#             response.msg = e
#         return Response(response.get_dic())
#         # return render(request, 'good/good_release.html', locals())
#
#     # 已完成 用于发布单个商品
#     def post(self, request):
#         '''
#         sell_method_choices = ((0, '同城当面交易'), (1, '快递'), (2, '不限交易方式'))
#         good_status_choices = ((0, '在售'), (1, '已售出'))
#         title = models.CharField(max_length=128, verbose_name='商品标题')
#         content = models.TextField(verbose_name='商品详情')
#         original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
#         current_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='现价')
#         sell_method = models.SmallIntegerField(choices=sell_method_choices, default=2, verbose_name='交易方式')
#         good_status = models.SmallIntegerField(choices=good_status_choices, default=0, verbose_name='商品状态')
#         owner_user = models.ForeignKey(to='user.User', related_name='good_owner_user', null=True, on_delete=models.SET_NULL,
#                                        db_constraint=False, verbose_name='商品发布者')
#         # 加一个关注商品的用户
#         star_users = models.ManyToManyField(to='user.User', related_name='good_star_users', db_constraint=False,
#                                             verbose_name='关注用户')
#         category = models.ForeignKey(to='Category', on_delete=models.SET_NULL, db_constraint=False)
#
#
#         image = models.ImageField(verbose_name='图片')
#         is_main_pic = models.BooleanField(default=0, verbose_name='是否是主图')
#         # 加外键关联商品
#         good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='对应商品')
#
#         :param request:
#         :return:
#         '''
#         # 先创建一个简单的回复对象,方便后续往里面放数据
#         response = CommonResponse()
#
#         # 尝试序列化组件
#         good_ser = GoodAndPictureSerializers(data=request.POST)
#         # 数据经序列化组件之后数据格式没问题的情况
#         if good_ser.is_valid():
#             # 经过序列化之后商品信息已经保存进数据库,并且通过django的model层返回了商品对象
#             good_obj = good_ser.save()
#             # 开始保存对应的图片类
#             # print(request.data['image'])
#             # 确认有几张图片,信息在request.data中对应的key下
#             image_name_list = request.data['image'].split(',')
#
#             # 在回复中添加images字典,用来保存照片保存成功与否的状态
#             setattr(response, 'data', {})
#             for image in image_name_list:
#                 # 所有文件都存在request.FILES中,每次循环获取一个对象
#                 image_obj = request.FILES.get(image)
#                 if image_obj and image_obj.size > 1 and image_obj.size < 20480000:
#                     # print(GOOD_IMAGE_DIR)
#                     # 需要修改文件名,确保图片文件名的不重复
#                     # 先取出文件后缀保留,之后还需要拼接回文件名中进行保存
#                     pic_back_end = image_obj.name.split('.')[-1]
#                     # 将文件名进行md5值+上传时间+用户id之后再加密
#                     image_name_md5 = hashlib.md5()
#                     name_bytes = '{}{}{}'.format(image_obj.name, time.time(), good_obj.owner_user.id).encode('utf-8')
#                     image_name_md5.update(name_bytes)
#                     # 使用md5的摘要值作为新的图片名
#                     new_image = image_name_md5.hexdigest()
#                     # 把文件后缀拼接回加密后的文件名
#                     new_image_name = '{}.{}'.format(new_image, pic_back_end)
#                     # print('new name', new_image_name)
#                     # 拼接出图片将保存的地址
#                     file_path = os.path.join(GOOD_IMAGE_DIR, new_image_name)
#
#                     # 使用文件路径保存文件
#                     path = default_storage.save(file_path, ContentFile(image_obj.read()))
#                     # tmp_file = os.path.join(settings.MEDIA_ROOT, path)
#
#                     # 图片保存成功后要保存进数据库了
#                     main_img = request.data.get('main_img')
#                     if image == main_img:
#                         GoodPictures.objects.create(image_path=file_path, is_main_pic=1, good=good_obj)
#                     else:
#                         GoodPictures.objects.create(image_path=file_path, is_main_pic=0, good=good_obj)
#             response.status = 200
#             response.msg = '商品信息接收成功'
#
#         # 序列化组件类的
#         else:
#             response.status = 100
#             response.msg = '商品数据格式错误'
#
#         return Response(response.get_dic())
#
#         # 准备好回复使用的response对象
#         # 开始接收商品表的信息
#
#
# class GoodEdit(APIView):
#     # 带有数据库的操作,先校验用户传来cookie中的token值
#     authentication_classes = [UserTokenAuth]
#
#     # 定义一个get函数,用来返回要编辑的商品的当前信息
#     def get(self, request, good_id):
#         response = CommonResponse()
#         try:
#             good_obj = Good.objects.get(pk=good_id)
#             if request.user_id == good_obj.owner_user.id:
#                 good_ser = GoodSerializers(instance=good_obj)
#                 # print(good_ser.data)
#
#                 # 将商品当前信息转换成字典形式保存在data中
#                 response.data = {**good_ser.data}
#
#                 response.data['images'] = {}
#                 response.data['images']['main_pic'] = None
#
#                 # 保存当前的商品返回给前台
#                 good_pics = GoodPictures.objects.filter(good=good_obj)
#                 # 遍历商品对应的所有图片,把图片的访问路径拼接后返回前台
#                 for p in good_pics:  # type:GoodPictures
#                     pic_url = '{}{}'.format(base_url, 'pic/{}'.format(p.id))
#                     print(pic_url)
#                     response.data['images'][p.id] = pic_url
#
#                     if p.is_main_pic:
#                         response.data['images']['main_pic'] = p.id
#
#                 response.data['sell_method_and_status'] = {}
#                 response.data['category'] = {}
#                 # 返回所有交易方式
#                 sell_method_and_status = GoodStatusAndSellMethod.objects.all()
#                 for s in sell_method_and_status:
#                     response.data['sell_method_and_status'][s.id] = s.status_content
#
#                 # 返回所有分类
#                 catecory_lists = Category.objects.all()
#                 for c in catecory_lists:
#                     response.data['category'][c.id] = c.name
#
#                 response.status = 200
#                 response.msg = '获取商品信息成功'
#
#         except Exception as e:
#             print(e)
#             response.msg = str(e)
#
#         return Response(response.get_dic())
#
#     # 将接收的信息进行单商品更新
#     # 更新(已完成)
#     def put(self, request, good_id):
#         response = CommonResponse()
#
#         # 尝试序列化组件
#         try:
#             good_obj = Good.objects.filter(pk=good_id)
#
#             good_ser = GoodAndPictureSerializers(instance=good_obj, data=request.data)
#             # 数据经序列化组件之后数据格式没问题的情况
#             if good_ser.is_valid():
#                 # print(good_ser.validated_data)
#                 good_ser.save()
#
#                 # print(good_ser.data)
#
#                 # 经过序列化之后商品信息已经保存进数据库,并且通过django的model层返回了商品对象
#                 # good_obj = good_ser.save()
#                 # print(good_obj.data)
#                 # 开始保存对应的图片类
#                 # print(request.data['image'])
#                 # 确认有几张图片,信息在request.data中对应的key下
#                 image_name_list = request.data['image'].split(',')
#
#                 # 在回复中添加images字典,用来保存照片保存成功与否的状态
#                 setattr(response, 'data', {})
#                 # 在更新方法中填写图片的id值
#                 for image in image_name_list:
#                     # 所有文件都存在request.FILES中,每次循环获取一个对象
#                     image_obj = request.FILES.get(image)
#                     if image_obj and image_obj.size > 1 and image_obj.size < 20480000:
#                         # print(GOOD_IMAGE_DIR)
#                         # 需要修改文件名,确保图片文件名的不重复
#                         # 先取出文件后缀保留,之后还需要拼接回文件名中进行保存
#                         pic_back_end = image_obj.name.split('.')[-1]
#                         # 将文件名进行md5值+上传时间+用户id之后再加密
#                         image_name_md5 = hashlib.md5()
#                         name_bytes = '{}{}{}'.format(image_obj.name, time.time(),
#                                                      good_obj.first().owner_user.id).encode('utf-8')
#                         image_name_md5.update(name_bytes)
#                         # 使用md5的摘要值作为新的图片名
#                         new_image = image_name_md5.hexdigest()
#                         # 把文件后缀拼接回加密后的文件名
#                         new_image_name = '{}.{}'.format(new_image, pic_back_end)
#                         # print('new name', new_image_name)
#                         # 拼接出图片将保存的地址
#                         file_path = os.path.join(GOOD_IMAGE_DIR, new_image_name)
#
#                         # 使用文件路径保存文件
#                         path = default_storage.save(file_path, ContentFile(image_obj.read()))
#                         # tmp_file = os.path.join(settings.MEDIA_ROOT, path)
#
#                         # 删除原图片id路径的图片
#                         modify_pic_obj = GoodPictures.objects.filter(pk=image).first()
#                         if modify_pic_obj:
#                             remove_path = modify_pic_obj.image_path
#                             print(remove_path)
#                             os.remove(remove_path)
#                             print('原图片删除成功')
#                         # 图片保存成功后要保存进数据库了
#                         main_img = request.data.get('main_img')
#                         if image == main_img:
#                             GoodPictures.objects.filter(pk=image).update(image_path=file_path, is_main_pic=1,
#                                                                          good=good_obj.first())
#                         else:
#                             GoodPictures.objects.filter(pk=image).update(image_path=file_path, is_main_pic=0,
#                                                                          good=good_obj.first())
#                 response.status = 200
#                 response.msg = '商品信息接收成功'
#                 # 序列化组件类的
#             else:
#                 response.status = 100
#                 response.msg = '商品数据格式错误'
#
#         except Exception as e:
#             response.msg = '更新商品错误'
#             return Response(response.get_dic())
#
#         return Response(response.get_dic())
#
#     # 删除一个商品(已完成) 不会删除数据库数据,只是修改商品状态,让商品不会显示,对应的图片不需要额外操作
#     def delete(self, request, good_id):
#         response = CommonResponse()
#         try:
#             good_obj = Good.objects.filter(pk=good_id).first()
#             if request.user_id == good_obj.owner_user.id:
#                 delete_status = GoodStatusAndSellMethod.objects.get(status_content='审核失败')
#                 Good.objects.filter(pk=good_id).update(good_status=delete_status)
#                 response.status = 200
#                 response.msg = '删除成功'
#             else:
#                 response.status = 101
#                 response.msg = '删除失败'
#         except Exception as e:
#             print(e)
#             response.msg = str(e)
#
#         return Response(response.get_dic())
#
#
# # 用于获取单张图片使用的视图
# class GetPicById(View):
#     authentication_classes = [UserTokenAuth]
#
#     # (已完成) 发送get请求时获取图片的内容
#     def get(self, request, pic_id):
#         try:
#
#             pic_obj = GoodPictures.objects.get(pk=pic_id)
#             print('pic_obj', pic_obj)
#             with open(pic_obj.image_path, 'rb') as f:
#                 response = HttpResponse(f)
#                 response['content_type'] = "application/octet-stream"
#                 response['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(pic_obj.image_path))
#                 return response
#         except Exception as e:
#             print(e)
#             return HttpResponse(str(e))
from django.shortcuts import render
from good.models import Good
def test(request):
    good_list = Good.objects.all()
    for g in good_list:
        print(g)

    return render(request, 'my_test.html', locals())