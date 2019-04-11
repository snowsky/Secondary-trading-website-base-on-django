import os
import hashlib
import time
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from user.utils.common_response import CommonResponse
from user.utils.user_drf_auth import UserTokenAuth
from salt_fish.settings import GOOD_IMAGE_DIR
from good.models import GoodPictures, Category, Good


class GoodDetail(APIView):
    # 单商品详情页面
    def get(self, request, pk):
        return render(request, 'good_detail.html', locals())


class GoodRelease(APIView):
    authentication_classes = [UserTokenAuth]

    # 获取发布商品的页面
    def get(self, request):
        response = CommonResponse()
        # 校验完要取出当前用户的id,方便后续POST发数据回来的操作

        # 返回所有交易方式
        sell_method = Good.objects.all().values('sell_method_choices')
        print(sell_method)

        # 返回商品的所有分类,供用户在前台选择发布到哪个分类下
        category_list = Category.objects.all()
        for c in category_list:
            print(c)

        response.status = 200
        return Response(response.get_dic())
        # return render(request, 'good/good_release.html', locals())

    # 已完成
    def post(self, request):
        '''
        sell_method_choices = ((0, '同城当面交易'), (1, '快递'), (2, '不限交易方式'))
        good_status_choices = ((0, '在售'), (1, '已售出'))
        title = models.CharField(max_length=128, verbose_name='商品标题')
        content = models.TextField(verbose_name='商品详情')
        original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
        current_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='现价')
        sell_method = models.SmallIntegerField(choices=sell_method_choices, default=2, verbose_name='交易方式')
        good_status = models.SmallIntegerField(choices=good_status_choices, default=0, verbose_name='商品状态')
        owner_user = models.ForeignKey(to='user.User', related_name='good_owner_user', null=True, on_delete=models.SET_NULL,
                                       db_constraint=False, verbose_name='商品发布者')
        # 加一个关注商品的用户
        star_users = models.ManyToManyField(to='user.User', related_name='good_star_users', db_constraint=False,
                                            verbose_name='关注用户')
        category = models.ForeignKey(to='Category', on_delete=models.SET_NULL, db_constraint=False)


        image = models.ImageField(verbose_name='图片')
        is_main_pic = models.BooleanField(default=0, verbose_name='是否是主图')
        # 加外键关联商品
        good = models.ForeignKey(to='Good', null=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='对应商品')

        :param request:
        :return:
        '''
        # 先创建一个简单的回复对象,方便后续往里面放数据
        response = CommonResponse()

        # 尝试序列化组件
        from good.utils.good_serilization import GoodAndPictureSerializers
        good_ser = GoodAndPictureSerializers(data=request.POST)
        # 数据经序列化组件之后数据格式没问题的情况
        if good_ser.is_valid():
            # 经过序列化之后商品信息已经保存进数据库,并且通过django的model层返回了商品对象
            good_obj = good_ser.save()
            # 开始保存对应的图片类
            # print(request.data['image'])
            # 确认有几张图片,信息在request.data中对应的key下
            image_name_list = request.data['image'].split(',')

            # 在回复中添加images字典,用来保存照片保存成功与否的状态
            setattr(response, 'data', {})
            for image in image_name_list:
                # 所有文件都存在request.FILES中,每次循环获取一个对象
                image_obj = request.FILES.get(image)
                if image_obj and image_obj.size > 1 and image_obj.size < 20480000:
                    # print(GOOD_IMAGE_DIR)
                    # 需要修改文件名,确保图片文件名的不重复
                    # 先取出文件后缀保留,之后还需要拼接回文件名中进行保存
                    pic_back_end = image_obj.name.split('.')[-1]
                    # 将文件名进行md5值+上传时间+用户id之后再加密
                    image_name_md5 = hashlib.md5()
                    name_bytes = '{}{}{}'.format(image_obj.name, time.time(), good_obj.owner_user.id).encode('utf-8')
                    image_name_md5.update(name_bytes)
                    # 使用md5的摘要值作为新的图片名
                    new_image = image_name_md5.hexdigest()
                    # 把文件后缀拼接回加密后的文件名
                    new_image_name = '{}.{}'.format(new_image, pic_back_end)
                    # print('new name', new_image_name)
                    # 拼接出图片将保存的地址
                    file_path = os.path.join(GOOD_IMAGE_DIR, new_image_name)

                    # 使用文件路径保存文件
                    path = default_storage.save(file_path, ContentFile(image_obj.read()))
                    # tmp_file = os.path.join(settings.MEDIA_ROOT, path)

                    # 图片保存成功后要保存进数据库了
                    main_img = request.data.get('main_img')
                    if image == main_img:
                        GoodPictures.objects.create(image_path=file_path, is_main_pic=1, good=good_obj)
                    else:
                        GoodPictures.objects.create(image_path=file_path, is_main_pic=0, good=good_obj)
            response.status = 200
            response.msg = '商品信息接收成功'

        # 序列化组件类的
        else:
            response.status = 100
            response.msg = '商品数据格式错误'

        return Response(response.get_dic())

        # 准备好回复使用的response对象
        # 开始接收商品表的信息
        # title = request.POST.get('title', None)
        # content = request.POST.get('content', None)
        # original_price = request.POST.get('original_price', None)
        # current_price = request.POST.get('current_price', None)
        # # sell_method有默认值,但如果用户修改的话,就会改变值
        # sell_method = request.POST.get('sell_method', None)
        # owner_user = request.user_id
        # category = request.POST.get('category', None)
        # print('title', title)
        # print('content', content)
        # print('original_price', original_price)
        # print('current_price', current_price)
        # print('sell_method', sell_method)
        # print('owner_user', owner_user)
        # print('category', category)
        #
        # # 开始接收商品照片表的信息
        # image1 = request.FILES.get('image1')
        # image1_is_main_pic = request.POST.get('image1_status')
        # image2 = request.FILES.get('image2')
        # image3 = request.FILES.get('image3')
        # image4 = request.FILES.get('image4')
        # image5 = request.FILES.get('image5')
        # print(image1)
        # print(image1.size)
        # print(image1_is_main_pic)
        # if image1.size > 1 and image1.size < 20480000:
        #     print(GOOD_IMAGE_DIR)
        #     path = default_storage.save(os.path.join(GOOD_IMAGE_DIR, image1.name), ContentFile(image1.read()))
        #     tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        #     response.data = '图片保存成功'
        # print(image2)
        # print(image3)
        # print(image4)
        # print(image5)


class GoodEdit(APIView):
    # 带有数据库的操作,先校验用户传来cookie中的token值
    authentication_classes = [UserTokenAuth]

    # # 根据传来的信息发布单个商品
    # def post(self, request, pk):
    #     # 准备好回复使用的response对象
    #     # title  = request.POST.get('title', None)
    #     # content  = request.POST.get('content', None)
    #     # title  = request.POST.get('title', None)
    #     # title  = request.POST.get('title', None)
    #     # title  = request.POST.get('title', None)
    #     # picture = request.POST
    #     response = CommonResponse()
    #     response.data = 'ok'
    #
    #     # 将对象的键值对作为字典返回
    #     return Response(response.get_dic())

    # 将接收的信息进行单商品更新
    # 更新
    def put(self, request, pk):
        response = CommonResponse()
        return Response(response.get_dic())

    # 删除一本书
    def delete(self, request, pk):
        response = CommonResponse()
        return Response(response.get_dic())
