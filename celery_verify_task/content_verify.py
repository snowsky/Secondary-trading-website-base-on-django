# -!- coding: utf-8 -!- # 字符串中有中文,写上后让python好截断其中内容


# 定义校验类,其中设置了英文与中文敏感词字典,传值进来后进行文字的验证
# 如果内容没有问题返回
class ArticleSafe:
    def __init__(self):
        self.chinese_safe_dict = '''三个代表,一党,多党,民主,专政,政治,大法,弟子,大纪元,真善忍,明慧,大法,洪志,红志,洪智,红智,法 轮,法论,法沦,法伦,发轮,发论,发沦,发伦,轮功,轮公,轮攻,沦功,沦公,沦攻,论攻,论功,论公,伦攻,伦功,伦公,打倒,民运,六四,台独,王 丹,柴玲,李鹏,天安门,江泽民,朱容基,朱镕基,李长春,李瑞环,胡锦涛,魏京生,台湾独立,藏独,西藏独立,疆独,新疆独立,警察,民警,公安,邓小 平,大盖帽,革命,武警,黑社会,交警,消防队,刑警,公款,首长,书记,腐败,城管,暴动,暴乱,李远哲,司法警官,高干,人大,尉健行,李岚清,黄丽 满,于幼军,文字狱,宋祖英,天安门,自焚,骗局,猫肉,吸储,张五常,张丕林,空难,温家宝,吴邦国,曾庆红,黄菊,罗干,吴官正,贾庆林,专制,三個 代表,一黨,多黨,民主,專政,大法,弟子,大紀元,真善忍,明慧,洪志,紅志,洪智,紅智,法輪,法論,法淪,法倫,發輪,發論,發淪,發倫,輪功,輪 公,輪攻,淪功,淪公,淪攻,論攻,論功,論公,倫攻,倫功,倫公,打倒,民運,六四,台獨,王丹,柴玲,李鵬,天安門,江澤民,朱容基,朱鎔基,李長 春,李瑞環,胡錦濤,魏京生,臺灣獨立,藏獨,西藏獨立,疆獨,新疆獨立,警察,民警,公安,鄧小平,大蓋帽,革命,武警,黑社會,交警,消防隊,刑警, 公款,首長,書記,腐敗,城管,暴動,暴亂,李遠哲,司法警官,高幹,人大,尉健行,李嵐清,黃麗滿,於幼軍,文字獄,天安門,自焚,騙局,貓肉,吸儲, 張五常,張丕林,空難,溫家寶,吳邦國,曾慶紅,黃菊,羅幹,賈慶林,專制,八九,八老,巴赫,白立朴,白梦,白皮书,保钓,鲍戈,鲍彤,暴乱,暴政,北 大三角地论坛,北韩,北京当局,北京之春,北美自由论坛,博讯,蔡崇国,藏独,曹长青,曹刚川,柴玲,常劲,陈炳基,陈军,陈蒙,陈破空,陈希同,陈小 同,陈宣良,陈一谘,陈总统,程凯,程铁军,程真,迟浩田,持不同政见,赤匪,赤化,春夏自由论坛,达赖,大参考,大纪元新闻网,大纪园,大家论坛,大 史,大史记,大史纪,大中国论坛,大中华论坛,大众真人真事,戴相龙,弹劾,登辉,邓笑贫,迪里夏提,地下教会,地下刊物,第四代,电视流氓,钓鱼岛,丁 关根,丁元,丁子霖,东北独立,东方红时空,东方时空,东南西北论谈,东社,东土耳其斯坦,东西南北论坛,动乱,独裁,独夫,独立台湾会,独立中文笔会, 杜智富,多维,屙民,俄国,发愣,发轮,发正念,反封锁技术,反腐败论坛,反攻,反共,反人类,反社会,方励之,方舟子,飞扬论坛,斐得勒,费良勇,分家 在,分裂,粉饰太平,风雨神州,风雨神州论坛,封从德,封杀,冯东海,冯素英,佛展千手法,付申奇,傅申奇,傅志寰,高官,高文谦,高薪养廉,高瞻,高自 联,戈扬,鸽派,歌功颂德,蛤蟆,个人崇拜,工自联,功法,共产,共党,共匪,共狗,共军,关卓中,贯通两极法,广闻,郭伯雄,郭罗基,郭平,郭岩华,国 家安全,国家机密,国军,国贼,韩东方,韩联潮,何德普,何勇,河殇,红色恐怖,宏法,洪传,洪吟,洪哲胜,洪志,胡紧掏,胡锦涛,胡锦滔,胡锦淘,胡景 涛,胡平,胡总书记,护法,华建敏,华通时事论坛,华夏文摘,华语世界论坛,华岳时事论坛,黄慈萍,黄祸,黄菊,黄翔,回民暴动,悔过书,鸡毛信文汇,姬 胜德,积克馆,基督,贾庆林,贾廷安,贾育台,建国党,江core,江八点,江流氓,江罗,江绵恒,江青,江戏子,江则民,江泽慧,江泽民,江澤民,江 贼,江贼民,江折民,江猪,江猪媳,江主席,姜春云,将则民,僵贼,僵贼民,疆独,讲法,酱猪媳,交班,教养院,接班,揭批书,金尧如,锦涛,禁看,经 文,开放杂志,看中国,抗议,邝锦文,劳动教养所,劳改,劳教,老江,老毛,黎安友,李长春,李大师,李登辉,李红痔,李宏志,李洪宽,李继耐,李兰菊, 李岚清,李老师,李录,李禄,李鹏,李瑞环,李少民,李淑娴,李旺阳,李文斌,李小朋,李小鹏,李月月鸟,李志绥,李总理,李总统,连胜德,联总,廉政大 论坛,炼功,梁光烈,梁擎墩,两岸关系,两岸三地论坛,两个中国,两会,两会报道,两会新闻,廖锡龙,林保华,林长盛,林樵清,林慎立,凌锋,刘宾深,刘 宾雁,刘刚,刘国凯,刘华清,刘俊国,刘凯中,刘千石,刘青,刘山青,刘士贤,刘文胜,刘晓波,刘晓竹,刘永川,流亡,六四,陆委会,吕京花,吕秀莲,抡 功,伦功,轮大,轮功,罗干,罗礼诗,马大维,马良骏,马三家,马时敏,卖国,毛厕洞,毛贼东,美国参考,美国之音,蒙独,蒙古独立,密穴,绵恒,民国, 民进党,民联,民意,民意论坛,民运,民阵,民猪,民主,民主墙,民族矛盾,明慧,莫伟强,木犀地,木子论坛,南大自由论坛,闹事,倪育贤,你说我说论 坛,潘国平,泡沫经济,迫害,祁建,齐墨,钱达,钱国梁,钱其琛,抢粮记,乔石,亲美,钦本立,秦晋,轻舟快讯,情妇,庆红,全国两会,热比娅,热站政论 网,人民报,人民内情真相,人民真实,人民之声论坛,人权,瑞士金融大学,善恶有报,上海帮,上海孤儿院,邵家健,神通加持法,沈彤,升天,盛华仁,盛 雪,师父,石戈,时代论坛,时事论坛,世界经济导报,事实独立,双十节,水扁,税力,司马晋,司马璐,司徒华,斯诺,四川独立,宋平,宋书元,宋祖英,苏 绍智,苏晓康,台独,台盟,台湾独立,台湾狗,台湾建国运动组织,台湾青年独立联盟,台湾政论区,台湾自由联盟,太子党,汤光中,唐柏桥,唐捷,滕文生, 天安门,天怒,天葬,童屹,统独,统独论坛,统战,屠杀,外交论坛,外交与方略,万润南,万维读者论坛,万晓东,汪岷,王宝森,王炳章,王策,王超华,王 丹,王辅臣,王刚,王涵万,王沪宁,王军涛,王力雄,王瑞林,王润生,王若望,王希哲,王秀丽,王冶坪,网特,尉健行,魏京生,魏新生,温家宝,温元凯, 文革,无界浏览器,吴百益,吴邦国,吴方城,吴官正,吴弘达,吴宏达,吴仁华,吴学灿,吴学璨,吾尔开希,五不,伍凡,西藏,西藏独立,洗脑,下体,项怀 诚,项小吉,小参考,肖强,邪恶,谢长廷,谢选骏,谢中之,辛灏年,新观察论坛,新华举报,新华内情,新华通论坛,新疆独立,新生网,新闻封锁,新语丝, 信用危机,邢铮,熊炎,熊焱,修炼,徐邦秦,徐才厚,徐匡迪,徐水良,许家屯,薛伟,学潮,学联,学习班,学运,学自联,雪山狮子,严家其,严家祺,阎明 复,央视内部晚会,杨怀安,杨建利,杨巍,杨月清,杨周,姚月谦,夜话紫禁城,一中一台,义解,亦凡,异见人士,异议人士,易丹轩,易志熹,尹庆民,由喜 贵,游行,于大海,于浩成,余英时,舆论,舆论反制,宇明网,圆满,远志明,岳武,在十月,则民,择民,泽民,贼民,曾培炎,曾庆红,张伯笠,张钢,张宏 堡,张健,张林,张万年,张伟国,张昭富,张志清,赵海青,赵南,赵品潞,赵晓微,赵紫阳,哲民,真善忍,真相,真象,镇压,争鸣论坛,正见网,郑义,正义党论坛'''
        self.english_safe_dict = '''bitch, shit, falun, tianwang, cdjp, bignews, playboy, renmingbao, rfa, safeweb,sex, simple, svdc, taip, tibetalk, triangle, triangleboy, UltraSurf, unixbox, ustibet, voa, wangce, wstaiji, xinsheng, yuming, zhengjian, zhengjianwang, zhenshanren, zhuanfalun, anime, censor, hentai, [hz],（hz）,[av],（av）, [sm], （sm）, boxun, chinaliberal, chinamz, chinesenewsnet, cnd, creaders, dafa, dajiyuan, dfdz, dpp, falu, falun, falundafa, flg, freechina,freenet, fuck, GCD, gcd, hongzhi, hrichina, huanet, hypermart, incest, jiangdongriji, japan, lihongzhi, making, minghui, minghuinews, nacb, na？ve, nmis, paper, peacehall, playboy, renminbao, renmingbao, rfa, safeweb, sex, simple, svdc, taip, tibetalk, triangle, triangleboy, UltraSurf, unixbox, ustibet, voa, wangce, wstaiji, xinsheng, yuming, zhengjian, zhengjianwang, zhenshanren,zhuanfalun,xxx,anime,censor,hentai,[hz],（hz）,[av],（av）,[sm], （sm）,porn,multimedia,toolbar,downloader'''
        self.safe_dict = {}
        # print(self.chinese_safe_dict.split(','))

    # 对外做成属性访问的函数,获取要进行校验使用的字典
    @property
    def safe_dict_content(self):
        chinese_safe_list = self.chinese_safe_dict.split(',')
        # print(chinese_safe_list)
        english_safe_list = self.english_safe_dict.split(', ')
        # print(english_safe_list)
        chinese_safe_list.extend(english_safe_list)
        self.safe_dict = chinese_safe_list
        # print(self.safe_dict)
        return self.safe_dict

    # 将要校验的文本作为参数传进来,可以
    def pure_article_without_punc(self, text):
        from string import punctuation
        add_punc = '，。、【】“”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=擅长于的&#@￥'  # 自定义--中文的字符
        all_punc = punctuation + add_punc
        temp = []
        for c in text:
            if c not in all_punc:
                temp.append(c)
        newText = ''.join(temp)
        newText = ''.join(newText.split())
        # print(newText)
        return newText

    def check_article_safe(self, verify_text, safe_dict):

        for word in safe_dict:
            if word in verify_text:
                return True
        else:
            return False


if __name__ == '__main__':
    a = ArticleSafe()
    # print(a.pure_article_without_punc(r'/.三个代表'))
    s = '{})  三,个 ) 代 % 表'
    # 使用方法
    # 先将输入文本去除标点及空格
    pure_text = a.pure_article_without_punc(s)
    print(pure_text)
    # 将无间隔的纯文本文字进行关键词的校验
    print(a.check_article_safe(pure_text, a.safe_dict_content))