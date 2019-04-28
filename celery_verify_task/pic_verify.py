# 单文件测试函数时需要配置的django设置
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
from good.models import GoodPictures

from PIL import Image
from collections import namedtuple


# 传递图片路径参数
class PicVerify:
    Skin = namedtuple('Skin', 'id skin region x y')

    # 校验类对象初始化时传入图片的path_or二进制数据,根据传入数据做判断

    def __init__(self, pic_path_or_pic):
        # 是对象的话直接打开
        if isinstance(pic_path_or_pic, Image.Image):
            self.image = pic_path_or_pic
        elif isinstance(pic_path_or_pic, str):
            self.image = Image.open(pic_path_or_pic)

        # 获取rgb通道,为了获取图片的宽和高
        bands = self.image.getbands()
        # 判断如果是灰度图, 转成rgb图
        if len(bands) == 1:
            new_image = Image.new('RGB', self.image.size)
            new_image.paste(self.image)
            f = self.image.filename
            # 将转换后的rgb图片替换image对象
            self.image = new_image
            self.image.filename = f

        # 准备存储找到的Skin皮肤像素点的列表
        self.skin_map = []

        # 元素的索引是皮肤的区域号,元素是一些匹配到的Skin皮肤对象的列表
        self.detected_region = []

        # 合并后的皮肤区域,索引是区域的编号,元素是Skin对象的列表
        self.merge_region = []

        # 合并后的皮肤区域,索引是区域的编号,元素是Skin对象的列表
        self.skin_region = []

        # # # 设置起始的区域编号
        self.region = 0

        # 当前图片的鉴定结果
        self.result = None

        # 当前图片的鉴定信息
        self.message = None

        # 用来记录最近一次的皮肤面积的合并的源头区域
        self.last_from = None

        # 用来记录最近一次的皮肤面积的合并的去向区域
        self.last_to = None

        # 获取图片的宽,高
        self.width, self.height = self.image.size

        # 保存图片的总像素
        self.total_pixels = self.width * self.height

    # 对尺寸较大的图片做压缩之后再做判断(可能对结果有影响)
    # 如果宽和高都不超过指定像素,返回值为0,如果只有宽超过,返回1,只有高超过返回2,宽高都超过返回3
    def resize(self, maxwidth=1000, maxheight=1000):
        ret = 0
        if self.width > maxwidth:
            width_compress_percent = (maxwidth / self.width)
            height_size = int(self.height * width_compress_percent)
            fname = self.image.filename
            # 使用Image的resize方法,调整图片的大小,解析器参数加上LANCZOS,这是Image的采样缩放算法
            self.image.resize((maxwidth, height_size), Image.LANCZOS)
            self.image.filename = fname
            self.width, self.height = self.image.size
            self.total_pixels = self.width * self.height
            ret += 1

        if self.height > maxheight:
            height_compress_precent = (maxheight / self.height)
            width_size = int(self.width * height_compress_precent)
            fname = self.image.filename
            self.image.resize((width_size, maxheight), Image.LANCZOS)
            self.image.filename = fname
            self.width, self.height = self.image.size
            self.total_pixels = self.width * self.height

            ret += 2
        return ret

    def parse(self):
        # 判断是否有结果,有结果直接返回当前判断类对象
        if self.result:
            return self
        # 如果还没有结果
        # 加载图片
        pixels = self.image.load()
        # 遍历所有的像素点的信息
        for y in range(self.height):
            for x in range(self.width):
                # 获取每个像素点的r,g,b的值
                r = pixels[x, y][0]  # red
                g = pixels[x, y][1]  # green
                b = pixels[x, y][2]  # blue
                # print(r, g, b)
                # 给每个Skin对象创建一个id,当前行像素加上列数*宽度,id从0开始,索引也从0开始
                # Skin = namedtuple('skin', 'id skin region x y')
                _id = x + y * self.width
                # True 表示是皮肤像素,需要处理,False表示非皮肤像素,不需要处理
                is_skin = True if self.verify_pixel(r, g, b) else False
                # print(is_skin)
                current_skin = self.Skin(_id, is_skin, None, x, y)

                # 将皮肤像素点Skin对象保存进skin_map矩阵中
                self.skin_map.append(current_skin)
                if not is_skin:
                    continue
                # 将检测到的当前像素点相邻的点检测一遍,看有没有region编号,如果有,就添加,如果碰到多个region纪要合并
                # 其中写条件表达式为了去除不连续的点
                check_nearby_index = [
                    (_id - 1) if (x % self.width) != 0 else None,  # 当前像素点的左侧的点(如果当前像素点在最左侧则没有左侧的像素点,为None)
                    (_id - 1 - self.width) if (x % self.width) != 0 else None,  # 当前像素点的左上的点(如果当前像素点在最左侧则不检查左上的像素点)
                    (_id - self.width),  # 当前像素点的正上的点
                    (_id - self.width + 1) if (x % (self.width - 1) != 0) else None  # 当前像素点的右上的点(如果当前点在最右侧则为None)
                ]
                # 每次循环重置当前区域号为-1
                region = -1

                # 开始遍历相邻点
                for index in check_nearby_index:

                    try:
                        self.skin_map[index]
                    # 从左向右扫描,最左侧点还没有,不用继续检测了
                    except IndexError:
                        break

                    # 如果相邻点是皮肤像素,那么就来尝试获取它的区域region值
                    if self.skin_map[index].skin:
                        # # 如果相邻的点的区域与现在的点的区域(region,self.skin_map[index])都是有效值,而且两个值不同,而且没有添加过(last_from,last_to)合并任务,就要做合并操作了
                        if (self.skin_map[index].region != None and self.skin_map[index].region != region \
                                and region != None and region != -1 and self.last_from != region \
                                and self.last_to != self.skin_map[index].region):
                            # 添加区域的合并任务, 除了最后一次循环的self.skin_map[index].region
                            self._add_merge_region(region, self.skin_map[index].region)
                        # 返回循环最后一次的区域号
                        region = self.skin_map[index].region

                # 相邻点的遍历循环结束,region还是-1,说明没有附近没有皮肤像素
                if region == -1:
                    # 接下来创建新的region区域号
                    region = len(self.detected_region)
                    # 元组不能直接修改属性
                    _skin = current_skin._replace(region=region)
                    # 更新skin_map中的数据
                    # Skin = namedtuple('skin', 'id skin region x y')
                    self.skin_map[current_skin.id] = _skin
                    # 在self.detected_region中添加新的区域列表,添加新的列表套元素到列表中,称为新的区域编号
                    self.detected_region.append([self.skin_map[current_skin.id]])

                # 不为-1且不为None, 说明从相邻点里取出了对应的区域号
                elif region != None:
                    _skin = current_skin._replace(region=region)
                    self.skin_map[current_skin.id] = _skin
                    # 向当前区域编号的列表中加数据,列表套列表的内层添加数据,区域编号是索引
                    self.detected_region[region].append(self.skin_map[current_skin.id])

        # 合并连接的区域
        self._merge(self.detected_region, self.merge_region)
        # 根据skin_region分析结果
        self.analyse_regions()

        return self

    # 对每一个像素点进行是否是皮肤的校验函数()
    def verify_pixel(self, r, g, b):
        # 由他人研究的算法公式写逻辑判断当前像素点的颜色是不是肤色
        rgb_verify_result = (r > 95) and (g > 40) and (b > 20) and ((max([r, g, b]) - min([r, g, b])) > 15) \
                            and (abs(r - g) > 15) and (r > g) and (r > b)

        return rgb_verify_result

    # merge_region = [[region_list1], [region_list2],...[region_listN]] 每个列表中的区域号是连接的,需要进行合并
    def _add_merge_region(self, _from, _to):
        self.last_from = _from
        self.last_to = _to

        # 合并的源头和去处,两个索引变量来标识
        from_index = -1
        to_index = -1

        # 先判断合并的数据有没有,有就会修改from_index和to_index的值
        # 假如传参进来的_from,_to代表的region区域号,已经在merge_region中了,
        # 操作merge_region的from_index和to_index会直接取出,为后续合并做准备
        for index, region in enumerate(self.merge_region):
            for r_index in region:
                if r_index == _from:
                    from_index = index
                if r_index == _to:
                    to_index = index

        # 函数传参来的_from和_to都已经在merge_region中时的操作
        if from_index != -1 and to_index != -1:
            # 如果是两个不同的区域,就要进行合并的操作了
            if from_index != to_index:
                self.merge_region[from_index].extend(self.merge_region[to_index])
                del self.merge_region[to_index]
            return

        # 如果传参来的_from和_to区域都不在现在的merge_region中
        if from_index == -1 and to_index == -1:
            # 在merge_region中添加一个新的列表,放着两个区域
            self.merge_region.append([_from, _to])
            return

        # 如果传参的有一个出现在merge_region中,from_index没找到,to_index找到
        if from_index == -1 and to_index != -1:
            self.merge_region[to_index].append(_from)
            return

        # 如果传参的有一个出现在merge_region中
        if from_index != -1 and to_index == -1:
            self.merge_region[from_index].append(_to)
            return

    # merge_region中只保存了区域编号,需要将编号对应的区域取出,merge_region中的一个元素是一个列表
    # 每个列表中的区域号对应的皮肤对象存在了detected_region中,所以要取出赋值给新的列表,最后保存在skin_region中
    def _merge(self, detected_region, merge_region):
        new_detected_region = []

        for index, region in enumerate(merge_region):
            try:
                new_detected_region[index]
            except IndexError:
                new_detected_region.append([])
            for r_index in region:
                # 遍历每个index的new_region中添加detected_region中r_index标识的每个skin对象
                new_detected_region[index].extend(detected_region[r_index])
                detected_region[r_index] = []

        # 如果有剩余皮肤区域,直接加进新列表
        for region in detected_region:
            new_detected_region.append(region)

        # 清理new_region列表
        self._clear_new_detected_region(new_detected_region)

    def _clear_new_detected_region(self, detected_region):
        for region in detected_region:
            # print(region, '++++++++++++++++++++++++++++++++++++++\n')
            # 只保留大于30个皮肤像素点的区域
            if len(region) > 30:
                # skin_region中是一个个列表,每个列表中是一个个skin对象
                self.skin_region.append(region)

    # 根据皮肤区域,得出结论
    def analyse_regions(self):
        # 如果皮肤区域数量小于3个
        if len(self.skin_region) > 3:
            self.message = '皮肤区域大于3个,目前是:{}个,不是yellow图'.format(len(self.skin_region))
            self.result = False
            return self.result

        self.skin_region = sorted(self.skin_region, key=lambda s: len(s), reverse=True)

        # 计算皮肤总像素数
        total_pixels = float(sum((len(region)) for region in self.skin_region))

        # 如果皮肤区域与整个图像的比值小于 15%，那么不是色情图片
        if total_pixels / self.total_pixels * 100 < 15:
            self.message = '照片的皮肤面积小于全图的百分之15,占比是:{}%.不是yellow图片'.format(int(total_pixels/self.total_pixels * 100))
            self.result = False
            return self.result

        # 如果最大皮肤区域小于总皮肤面积的 45%，不是色情图片
        if len(self.skin_region[0]) / total_pixels * 100 < 45:
            self.message = '照片的最大皮肤面积小于皮肤总面积的45%,占比是{}.不是yellow图片'.format(int(len(self.skin_region[0]) / total_pixels * 100))
            self.result = False
            return self.result

        # 皮肤区域数量超过 60个，不是色情图片
        if len(self.skin_region) > 60:
            self.message = '照片的皮肤区域数量超过60个,目前数量是:{}个.不是yellow图片'.format(len(self.skin_region))
            self.result = False
            return self.result

        self.message = '大兄弟,你在看神马刺激的呢!'
        self.result = True
        return self.result

    def verify_and_get_result_message(self):
        self.resize()
        self.parse()
        return self.result, self.message

    def showSkinRegions(self):
        if self.result is None:
            return
        skinIdSet = set()

        simage = self.image
        simageData = simage.load()

        for sr in self.skin_region:
            for pixel in sr:
                skinIdSet.add(pixel.id)

        for pixel in self.skin_map:
            if pixel.id not in skinIdSet:
                simageData[pixel.x, pixel.y] = 0, 0, 0
            else:
                simageData[pixel.x, pixel.y] = 255, 255, 255

        from io import BytesIO
        img_file = BytesIO()
        simage.save(img_file, 'JPEG')

        return img_file.getvalue()


if __name__ == '__main__':
    pic_obj = GoodPictures.objects.get(pk=15)
    pic_ver_obj = PicVerify(pic_obj.image_path)
    pic_ver_obj.resize()
    res = pic_ver_obj.parse()
    print(res.result)
    print(res.message)
