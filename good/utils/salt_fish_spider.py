import os
import sys
BASE_DIR = r'/home/cqh/python_project_dir/salt_fish/'
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salt_fish.settings")  # 项目名如果直接包含django,好像会报错,使用其他的名称正常
# 2. 启动Django
import django
import pymysql

pymysql.install_as_MySQLdb()
django.setup()
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time

from good.models import Good, GoodPictures, GoodStatusAndSellMethod, Category
from user.models import User
from salt_fish.settings import GOOD_IMAGE_DIR

# first_category = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[4]/p')
# first_category.click()
# print('进入手机分类页')
# driver.implicitly_wait(5)
#
# good_url_tags = driver.find_elements_by_xpath('/html/body/div[2]/div[4]/div/a')

# print(good_url_tags)

# good_url_set = set()

# for tag in good_url_tags:
#     tag_url = tag.get_attribute('href')
#     good_url_set.add(tag_url)
# print('爬完了第一页数据')
#
# print(good_url_set)
#
# next_page = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/ul/li[2]')
# next_page.click()
# print('跳到了第二页')
#
# driver.implicitly_wait(3)
# # 第二页的商品链接标签
# good_url_tags = driver.find_elements_by_xpath('/html/body/div[2]/div[4]/div/a')
#
# for tag in good_url_tags:
#     tag_url = tag.get_attribute('href')
#     good_url_set.add(tag_url)
#
# print('爬完了第二页的数据')
# print(good_url_set)
#
# # 第三页商品链接
#
# next_page = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/ul/li[3]')
# next_page.click()
# driver.implicitly_wait(3)
# print('跳转到了第三页')
# # 第三页的商品链接标签
# good_url_tags = driver.find_elements_by_xpath('/html/body/div[2]/div[4]/div/a')
#
# for tag in good_url_tags:
#     tag_url = tag.get_attribute('href')
#     good_url_set.add(tag_url)
#
# print(good_url_set)
#
# print('第三页爬取结束')

# 第四页
# next_page = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/ul/li[4]')
# next_page.click()
# driver.implicitly_wait(3)
# print('跳转第四页')
# good_url_tags = driver.find_elements_by_xpath('/html/body/div[2]/div[4]/div/a')
# for tag in good_url_tags:
#     tag_url = tag.get_attribute('href')
#     good_url_set.add(tag_url)
#
# print(good_url_set)
# print('第四页爬完')


# /html/body/div[2]/div[5]/div/ul/li[4]
# /html/body/div[2]/div[5]/div/ul/li[5]
# /html/body/div[2]/div[5]/div/ul/li[5]
# /html/body/div[2]/div[5]/div/ul/li[5]
# /html/body/div[2]/div[5]/div/ul/li[1]

good_url_set = set()
good_detail_dic = {}
# 记录爬取一个分类中几个页面的数据
count = 10


def get_crab_page():
    # 记录爬取的页数
    # 先获取页数前5页,xpath从'/html/body/div[2]/div[5]/div/ul/li[1]'到

    # '/html/body/div[2]/div[5]/div/ul/li[5]'
    global count

    for i in range(1, count + 1):
        # if i < 6:
        if i == 1:
            time.sleep(2)
            print('当前爬取第{}页'.format(i))
            yield
        else:
            # / html / body / div[2] / div[5] / div / button[2] / i
            # '/html/body/div[2]/div[5]/div/button[2]'
            page = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/button[2]')
            # page = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/ul/li[{}]'.format(i))

            # page.click()
            page.send_keys(Keys.ENTER)
            # driver.implicitly_wait(3)
            time.sleep(2)
            print('当前爬取第{}页'.format(i))
            yield page


def get_url_in_page():
    # 获取当前页面的所有的商品标签

    good_url_tags = driver.find_elements_by_xpath('/html/body/div[2]/div[4]/div/a')
    for tag in good_url_tags:
        good_url = tag.get_attribute('href')
        good_url_set.add(good_url)

    # print(good_url_set)
    # print(len(good_url_set))


# 最终要爬到的信息title, content, price,以及图片的url连接
def get_detail_info_by_url(good_set):
    for link in good_set:
        driver.get(link)
        # time.sleep(1)
        driver.implicitly_wait(1)

        # 当前链接的商品标题
        title = driver.find_element_by_xpath('//*[@id="J_Property"]/h1').text
        # print(title)
        # 当前链接的商品内容
        content = driver.find_element_by_xpath('//*[@id="J_DescContent"]').text
        # print(content)
        # 当前链接的商品价格
        price = driver.find_element_by_xpath('//*[@id="J_Property"]/ul[1]/li/span[2]/em').text
        # print(price)

        # 当前商品的所有图片标签
        img_url = driver.find_element_by_class_name('big-img').get_attribute('src')

        # print(img_url)

        good_detail_dic[len(good_detail_dic) + 1] = {'title': title,
                                                     'content': content,
                                                     'price': price,
                                                     'img_url': img_url}


# 将字典信息对应着存进数据库中
def add_crab_info_to_db(good_info_dic):
    for i in range(1, len(good_detail_dic) + 1):
        info_dic = good_detail_dic[i]
        '''
        title content  original_price current_price  sell_method 
        good_status owner_user star_users category
        '''
        sell_method = GoodStatusAndSellMethod.objects.get(status_content='不限交易方式')
        good_status = GoodStatusAndSellMethod.objects.get(status_content='已发布')
        owner_user = User.objects.get(pk=1)
        category = Category.objects.get(name='手机')
        good_obj = Good.objects.create(title=info_dic['title'], content=info_dic['content'],
                                       original_price=info_dic['price'], current_price=info_dic['price'],
                                       sell_method=sell_method, good_status=good_status, owner_user=owner_user,
                                       category=category)

        print(good_obj)
        # 要保存图片
        import urllib.request
        import hashlib
        # 网络上图片的地址
        img_src = info_dic['img_url']
        pic_back_end = img_src.split('.')[-1]

        # 创建照片的文件名
        image_name_md5 = hashlib.md5()
        name_bytes = '{}{}{}'.format(img_src, time.time(), 1).encode('utf-8')
        # 创建图片的保存路径
        image_name_md5.update(name_bytes)
        new_image = image_name_md5.hexdigest()
        new_image_name = '{}.{}'.format(new_image, pic_back_end)

        # 文件的路径名,这是要保存的
        file_path = os.path.join(GOOD_IMAGE_DIR, new_image_name)

        # 将远程数据下载到本地，第二个参数就是要保存到本地的文件名
        urllib.request.urlretrieve(img_src, file_path)

        GoodPictures.objects.create(image_path=file_path, is_main_pic=1, good=good_obj)

        print('一个商品保存成功,一个突破保存成功')
        # break

        # if image_obj and image_obj.size > 1 and image_obj.size < 20480000:
        #     print('照片的size:{}|,================================='.format(image_obj.size))
        #     # print(GOOD_IMAGE_DIR)
        #     # 需要修改文件名,确保图片文件名的不重复
        #     # 先取出文件后缀保留,之后还需要拼接回文件名中进行保存
        #     pic_back_end = image_obj.name.split('.')[-1]
        #     # 将文件名进行md5值+上传时间+用户id之后再加密
        #     image_name_md5 = hashlib.md5()
        #     name_bytes = '{}{}{}'.format(image_obj.name, time.time(), good_obj.owner_user.id).encode(
        #         'utf-8')
        #     image_name_md5.update(name_bytes)
        #     # 使用md5的摘要值作为新的图片名
        #     new_image = image_name_md5.hexdigest()
        #     # 把文件后缀拼接回加密后的文件名
        #     new_image_name = '{}.{}'.format(new_image, pic_back_end)
        #     # print('new name', new_image_name)
        #     # 拼接出图片将保存的地址
        #     file_path = os.path.join(GOOD_IMAGE_DIR, new_image_name)

        # 使用文件路径保存文件
        # path = default_storage.save(file_path, ContentFile(image_obj.read()))
        # tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        # 图片保存成功后要保存进数据库了
        # main_img = request.data.get('main_img')
        # if image == main_img:
        #     GoodPictures.objects.create(image_path=file_path, is_main_pic=1, good=good_obj)
        # else:
        #     GoodPictures.objects.create(image_path=file_path, is_main_pic=0, good=good_obj)


# 之后的xpath都是'/html/body/div[2]/div[5]/div/ul/li[1]'


if __name__ == '__main__':
    print('start')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 可以提升速度
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = Chrome(options=chrome_options)
    salt_fish_url = 'https://2.taobao.com/'
    driver.get(salt_fish_url)
    driver.implicitly_wait(3)
    # 找到要爬取的分类
    category_tag = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[4]/p')
    # category_tag = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[5]/p')
    # 发送点击事件,进行跳转
    category_tag.click()
    print('进入改了手机分类页')
    # 如果网页加载,做显式等待
    driver.implicitly_wait(5)
    # 爬取一定页数的数据,用set集合类接受url地址进行去重
    for p in get_crab_page():
        get_url_in_page()

    # print(good_url_set)
    # 对set中的每一个url做get请求,在打开的页面爬取详细信息了
    get_detail_info_by_url(good_url_set)

    print(good_detail_dic)
    add_crab_info_to_db(good_detail_dic)

    # 要保存进数据看了,导入django的配置文件了
