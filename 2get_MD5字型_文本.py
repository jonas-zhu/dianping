"""partA：GlyphID 标签的name中的编码

partB：TTGlyph标签的所有内容

partC：百度识图出来和GlyphID 标签的name中的编码顺序一致的文本

事实上当前页面已经解析完了，编码和文本对应成功，写一个字典对应即可，
但是大众点评的不是每天都用同一套woff（每套woff里面的编码不同），
所以为了可持续发展，在有需要时可以快速构建编码和文本对应的新字典，
你还需要对partB下手,partB和partA可以映射，partA和partC可以映射，
所以C和B可映射，partB（字形）每次都是不变的，文本也是不变的，
最终你构建的是字形和文本的对应，这使你在编码变更时能快速获得最新的 编码和文本对应的新字典。
"""
import re
import hashlib
from bs4 import BeautifulSoup


# partA：获取GlyphID 标签的name中的编码
def get_name_id(path):
    with open(path, 'r', encoding='utf-8')as f:
        t = f.read()
    soup = BeautifulSoup(t, 'xml')
    names = [i['name'] for i in soup.find_all('GlyphID')]
    return names

# partB：TTGlyph标签的所有内容,name与字型做key-value。 {name:字型} 字型hash
def md5_code(path):
    with open(path, 'r', encoding='utf-8')as f:
        t = f.read()
    md5_list = {}
    soup = BeautifulSoup(t, 'xml')
    ttg_list = soup.find_all('TTGlyph')
    # print(str(ttg_list[2]))
    for ttg in ttg_list:
        tar = re.findall(r'name=".*?"', str(ttg))[0]    # name="unie011"
        name = re.findall(r'name="(.*?)"', str(ttg))[0] # unie011
        result = str(ttg).replace(tar, '')
        md5_code = hashlib.md5(result.encode(encoding='utf-8')).hexdigest()
        md5_list[name] = md5_code
    return md5_list
# &#xf3a0;      网页中的字符
if __name__ == '__main__':
    xml_path = './dianping1.xml'
    # 获取woff文件中name
    names = get_name_id(xml_path)[2:]
    # 获取woff文件中name-字型  key-value ，value用hash缩小字符，字型不会变
    md5_l = md5_code(xml_path)
    md5_sort = []
    for name in names:
        md5_sort.append(md5_l[name])
    # print(md5_sort)
    # 获取woff文件中映射的文字，与上面的name顺序一致，不会变
    words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花' \
            '专东肉菜学福饭人百餐茶务通昧所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批' \
            '坊州牛佳化五米修爱北养卖建材三会鸡室红站徳王光名 丽油院堂烧江社合星货型村自科快便日民营和活盦眀器烟育瑸精屋经居' \
            '庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加' \
            '麻联卫川泰色世方寓风幼羊烫来髙厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗' \
            '布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺內' \
            '侧元购前幢滨处向座下県凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝' \
            '峰六振珠局岗洲横边济井办汉代临弄团 外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个' \
            '也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想岀员两推做排实分间甜' \
            '度起满给热完格荐喝等其再几只现眀候样直而买于般豆量选奶圢每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带' \
            '虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晩微周值费性桌拍跟块调糕'

    words = words.replace('\n', '').replace(' ', '')
    # 根据字形 md5-文本 生成字典，然后后续生成 编码-文本 的字典
    dic = {}
    print(len(md5_sort))
    print(len(words))
    if len(words) == len(md5_sort):
        for m, w in zip(md5_sort, words):
            dic[m] = w
    print(dic)

"""   # ma5_字型：文本
    md5_dict = {'d9e14a02cd7ef6896f242f7a1a250ef4': '1', '0cc16e5f6b00319ae28c44106fe78869': '2',
                '2f9e68307bdd3ef01fa45eaea9a5c160': '3', '7f95bacc077b3de6d1c7a77ddcffd37d': '4',
                '6a064c660c4b1ef76c04cf71a94e4374': '5', '594d17741fd7a443b5752a6f77f1e05f': '6',
                'd60a74bd8f8ff62b2246cbd9001ffc56': '7', 'defe796199cf9491e2cf6b0c74f12822': '8',
                'fe938a9482a4682541dc6cd5282ccbf9': '9', '1a8a0633ae0fcd9ca1a4f8bda00493c5': '0',
                '3613cef90c19d9037a2413ad716100c4': '店', 'caf610dd7ac9b247100e277603e3b7fb': '中',
                '311103a33b16efde92a4cb71e88f842d': '美', '3a941e0b4deea30b12a3629a4ac697c5': '家',
                '2e152c896492b762371e8872a5db2ee0': '馆', '8614ab6f89ed84a3c341b0f5d280be86': '小',
                '246f3ce733804e350aecd03e7f622ae5': '车', 'd172cba044de20bdcf41e03dbc862d2c': '大',
                '5e9064499b98b0c0b5b8329cb155079f': '市', 'c0c849d03199c875bbc4961fce54fe58': '公',
                'e599b66f6b5a877d6082aa36f6e169f8': '酒', 'fc9eb836964878faecf28969e6e0c2c1': '行',
                'b91e61396e1bd75dbe3335099594079f': '国', '3e1e1d0b8444889eed4ea29784afd3c7': '品',
                'e433ff7065548b3bae32db2e6ac25ba0': '发', 'ec458d62e2ef8d23b0767dbc201d9ffe': '电',
                '947a8953ee3112303a595f2dd511166e': '金', 'd310759b32098bb3120182d1660bab94': '心',
                '85ab4d18f230be44b1b1a56f49500100': '业', '550b9d24c080c2b5170f376d281fb524': '商',
                '823508ec80d6a6eca5753958e166f0db': '司', '3a8d3aa8034c3dba0041c91da7142b64': '超',
                'a667f0a94df1350410f917c3ea9526e7': '生', 'cae6a3bc3c0fe863ddf5c844f43d19a2': '装',
                'b879fbed84147cca6e63baf7d3b4c94a': '园', '357191c63c511628ae86c36f1a25f9df': '场',
                '3a2730e5122400aefa33c1f80c8c0bc5': '食', '12c1e6db48141369a710824101babc05': '有',
                'e8e9ac3fc02c9d718a8d0ae4447be891': '新', 'de02a2b71eab4e6e507e1aa419e5b672': '限',
                'c2509687d4b83199c95e61dff7c22c8a': '天', '60b4bc2fea998893afa2ee0f2b2379a8': '面',
                'b3dd40988cdc65bc24f9c114cd2083df': '工', '4f3044932334f1c8ec6896833706e1ec': '服',
                'afd1eac03f38803b0a2869812a65d181': '海', '3ec31b177768473554ccfccacc2831b0': '华',
                '8f2d2f5295db39bd8160fbf463b3f478': '水', 'a3a0bb1d2197168427fd9280cc564a1b': '房',
                '352cb274d5b22ad2f43a2ccd1fa53b88': '饰', '998d190f46902454191f8545f3c04c25': '城',
                'c2eb5ef614f2188699a608741e9d4bf3': '乐', '736f132a22fb6b85c5da8e665d666b2c': '汽',
                '7e01835926819895f1207c6c684b0d6b': '香', '2552b126bdbab605d3c837e229c9ad58': '部',
                '6fe109c2865e3daa801395a49700a2c4': '利', 'c2d665a08117a643ffbbbd7ccacabc53': '子',
                'f9e1f73f4c1dd1024eb5b13bd326c14b': '老', 'a2b50e474630802755ddde9f18fb04ab': '艺',
                'b7dcec947814e2f2a89059f9add5e445': '花', '480352028a36cf66de01834d96b4463a': '专',
                '66ef54a35f60c4a2062ee038fc282d27': '东', '11ef92d4e53a9888638252c85ed20095': '肉',
                '31ba6f66d07fb5005931bbf27b758d45': '菜', '0b2bbabdad98965027fc5d08dff5450e': '学',
                '61dba42c7394ebac61e31d89f254fa8e': '福', '144c0d6af3e8c9bf99a37823283299ac': '饭',
                '1416c2cbcdd4dd47379558463bd7a771': '人', '381aaea0fd89ff20700d228a9427c837': '百',
                'bc446475b852a42b72667edeef43cf48': '餐', 'c26fcd3580e4c405291e5ce2c3e143ec': '茶',
                'c9738cf0f3ca2b61a570a87b9aba00c6': '务', 'e78a0f2f8e2993e8ebe63d0eccf25a96': '通',
                '30f79f3637358818e4692c0cd94c3eaf': '昧', 'cb9180fe79530d6b553d15e9b866a1ff': '所',
                'd5637fe4df77fcee9c220a1439e1b66f': '山', '21bba07414d270d47b7c405d230376c6': '区',
                '7e873474250281db0f86b2d66aa38ea2': '门', 'dbc6826ac55bc1e9c39b2eaf54cfc739': '药',
                '57fe9b1d6f47fe5a18a058d5282b2607': '银', 'b9fbd7b60d662def4168c2800db41aa0': '农',
                'd439d4da2447e9a71d119a7104be5632': '龙', '99ce9a4b6212c3716ab6f382aba4725b': '停',
                '6235e25f8d06b4114a314469abe9150d': '尚', 'd120f9689d478f4f43410c9c30dadd0f': '安',
                '06ed335cdb66c2aa2da136a5be541fe6': '广', 'ffe23ac74b3caed47adcfd9502eae4aa': '鑫',
                '5cd74a24b17753907ee20878ee1f4e87': '一', 'e0634707300ea62ed88053b31d8cec46': '容',
                '346a83a225dee3e166c78ca789d850a5': '动', '19eeeebbd6774b448984900bea2755c1': '南',
                'c7111b93704ea37cdb51dccc7a9693c3': '具', 'd382da2e2fef876773909cf03e8132dd': '源',
                '14cc1584194cd241879a5d38c587d029': '兴', '6d540a995306232c1e3e0e5aca567e20': '鲜',
                'd28c0ea9635bf9a8e1977383aa5800d0': '记', 'ca8cd410f54de4e17eaf4131978ec75f': '时',
                '1013b70496a1aca7392bcdbcba8464e6': '机', '671e01bf43ee59ae53de91e32730e047': '烤',
                '962da60efae564a13223e59f918d2e31': '文', '1beb89f1e09c45ee031694182a6d3aec': '康',
                '5abc76d0dcd029f1007a995d10e096fa': '信', '4f848623a063109720cb6cbc1b6b6c95': '果',
                'd1ecf0c87714bbc40e96738db11371dd': '阳', '9262e080f19e6e96cccd0640c99c9c98': '理',
                '1a750eaf63fde8893ac2975c6e8fb6cf': '锅', '836589a8486c261e3e47b2507b9f29e6': '宝',
                '260d2db1e1815e8cdb35cc718f0ac28d': '达', '38ab54be5c4cdf86c48d950678396e04': '地',
                '3b34e4058c1d321cf3c31d96b88f6870': '儿', 'fc7c27ee9cdce8189e90a307024923cd': '衣',
                '878bead37475ce370dce9f065c1fcb31': '特', '544b2e6d0b4f8e6157e170bdaa304118': '产',
                'd7037f25bc5c56d48e92b8d468dd51fa': '西', '75eb17eabb7492ab371b6f9324e7ad0c': '批',
                '5415eb99dcbdfb320915cf5d724fd979': '坊', 'd7a34bd797ece1da3345a651005b5aaa': '州',
                '85090cdb0e4659eb2d6d0a1144a71d2d': '牛', '8b0f0cd7ad855cf8b4f1d6f1e6ba381a': '佳',
                'a3b0598f33a7523a040ba1655ddd1628': '化', '9d19f02e3ff7bcc7bb6f952a80eb93f9': '五',
                '422da567eb8123981b415f3a8764a469': '米', 'c9c3d959551079fd2c685af43a8d03e8': '修',
                '304b1493edb41e37efff1c9aae2972b8': '爱', '6e0e3aed7b11f91da1c676e790e7e7c8': '北',
                'bf408e4a039444a36c6554e7c2d8a854': '养', 'ba79b8fc085d9e59b6a76ad58b5a0715': '卖',
                '94fc83cdce005a795d4a95b1b072b981': '建', '62fe96e8660dbcda11f85bd06d99a6ff': '材',
                '0856ca79342ce7a387357c2530c5b2e0': '三', '7edf3f5d3572872694eec90dbf3b7cc2': '会',
                'a539ae40fdb0e704dc676d35e3e79113': '鸡', '4645df05f78031e1927c57bb2d28c605': '室',
                'c3d9b92d6409b620c403bf67c0ba5b7a': '红', 'ef887d8e4595f69f936fff2c97341328': '站',
                '35da54d4f4e36a90bfbf03d7ce66608f': '徳', '37c2fbd5fb43f17764a0dbd708c2808a': '王',
                '1aaea923cdf5e1366d0e6c996cede217': '光', '0664980231c68d76419a9637de080c5d': '名',
                '74222dc560259e79135b5f5c7027095a': '丽', 'a0a8a0573e38c08f43400b858d678233': '油',
                'fa898cbaf198c11017be7ae9f454504c': '院', '75a9e22ed4f59411311414157ec06ac0': '堂',
                'e2eb3b512acf501f6c6c63492194ec97': '烧', 'd414bb004738cdda5a57932f4e7d26e5': '江',
                '8022b9b7b1c63a126fe55b9997ee40d1': '社', 'e16264d693b3b8e856a6913923e614f5': '合',
                '6854a93e106ef599507faa55194e3157': '星', 'cb6aca334e90832d0894257410b71377': '货',
                '9412eacb17680452503001699c06bcdf': '型', '5a52194dbbc3a591000343eb9a70ed63': '村',
                '0d3999aac61ef85a8034e05929ac1c05': '自', '3f91ff43505f19d6cb11954874eb3d98': '科',
                'bf342fb1e11de3e21fde43cb46a04db3': '快', '4f3cad0b48ef2188934cbee5ba0caa4a': '便',
                '4ad14cbfbc08a944ea02f1b4d202583e': '日', 'f16656512be085caf6d2d3f9bde9becb': '民',
                '931981a90f45156d5fa4fbb9f5776ab9': '营', 'f0cb712ca3ee61d5304d9f20d8e04bb2': '和',
                'd69ca32a324ee398f858ac7d9c37bf18': '活', '506e1decf2f2e4d8c9ef14ceae8c354c': '盦',
                '4243cbcf916ef8e38f54721f5ec43dd7': '眀', 'f601f6354ab23a6a53f700795d0493af': '器',
                'c6bee39ceca5eb0e8fccbe657c0a6146': '烟', '4bb654b5916235b6a56dfe701f41deb3': '育',
                '293a386053e7f61c59e444b3357fbbb4': '瑸', 'f21141c2720c73bc047579f857403332': '精',
                '42333ad8aa7971ec1bd60661b347aca9': '屋', 'c4f2fc245ee5c0878465d0f7c3b1963d': '经',
                '34b9adcb1a14b98aeeb3ad2fa605da7e': '居', '9b27481b883f7418910e8a6c71965e59': '庄',
                'f8f3f2d6475c91b961038bceb02d02ae': '石', '999c8f76c0a84508d6be42fa31dcf5d9': '顺',
                'd36e900e6124b2ad26eba48042b06262': '林', 'b31501060328b330f9d1eaeb00df6bf8': '尔',
                'ec28b8f9f681a92bb7e1a88e5fdde520': '县', '7bffad4c21340cc5918c57544b4a107d': '手',
                'f833ab6b9f66ba18f18585636e68605b': '厅', '7f92b2075efc8a060987e52a05d74f5b': '销',
                '9d5e0b072a70d59346ea0b68648b23e4': '用', '36024c2955dfb3d3b3d8b1d871c956f6': '好',
                'ad3f77e5a010d8654be71659122bb72f': '客', '5ec58907677b7bc6703d961a87445769': '火',
                'd206c0844fcb94dc72cad0b61af8d6e8': '雅', '4ae7a70900ffc2617ee1904d01f59f7b': '盛',
                '86b5f3f0d77ab5236c86e96b292cb385': '体', '687363f36edfa9cc0023e92591972628': '旅',
                'd49791dcd403eadffde4d9f59ec09212': '之', '5b5da37a3ac7ebcac27e63e04d3b0323': '鞋',
                '708492053d914d95ea156792835d3fe5': '辣', '30dc9cf855f78b34f203a8b7db2ee10e': '作',
                '461739d2d98e4c96f703eb9e219d1833': '粉', '5f1fb91baedefb7212636c47bd10db82': '包',
                '10620a5a66b8347a1cca1ed30914d9a1': '楼', '2af32e39dc830a0288cd5e61fbba36ed': '校',
                '8ad92418d0e596caa8276cc8dbf99d16': '鱼', 'c869dac44fe95545a1fc8ceb690eacb4': '平',
                'bfb109d95376e6edd5c015d2c3f24a15': '彩', 'a7e074e37a83a0d038255885e253f984': '上',
                'dbf5c41bff7d8e9f46fdaf5758020022': '吧', '64b481aa47454249ac144926971b474b': '保',
                '5447771e804a580487c13886e1bcc012': '永', 'b56ffdf41bbe9f21bf995827845368ac': '万',
                '16be3a10622a481e25b0335eaa4d59f6': '物', '3f0df72424a5c3601dd701bcb6c7e2e2': '教',
                '221b7e198cccb58a5a0dbcac0f56bf28': '吃', '32225c1d9c22c0e890599309dcaa48b3': '设',
                '569f077ba7c211dd1db24b1de909b107': '医', '94e120952b2c1da17b291eb8279e8e6a': '正',
                '697f902b23ceaf2a5e8429c1b8d29d7b': '造', '656de65ec87e0675d1c64487d56bba59': '丰',
                '3aad5c7315f37ed1b462b14547137048': '健', '73c63f8353ec57e7a7e0940c04b5586a': '点',
                'eac19a4de24166c0c34204f7d7129df0': '汤', 'b138f69e4a316d42c2fb0a9830f0faf0': '网',
                'fa4fb3f9fdc0dc1255a1f942c72134f5': '庆', 'c4de5cc0f86aa61be8388469461a6803': '技',
                '25b268f91719ff08d540eb05d92b3695': '斯', '2942be2ebe6ca8659c098892c4c2a2eb': '洗',
                'fff9522737ecc4f7a87758d22688b083': '料', '280a515dd96cb98e74ea1b08b5dab9c1': '配',
                '9a885a98d240dc43b9482b37af328d95': '汇', '42c5e2c36aba2b56353b49aa7e7d7c35': '木',
                '2fd015e9ddb6d65e81916dc637f92f21': '缘', 'c8d6b2d87998a28c289ca728af5704fa': '加',
                'f4d9efa511813ffa7ab03947b9139d97': '麻', '7e0f2446b44c431b7c3625c1a9abd26e': '联',
                'd0de87f682a06afd97e436ed0115e151': '卫', 'b1191855fa8ae3a8a1fffafb47955732': '川',
                '5925164762ca0dbc6f1644268bece2fc': '泰', '263a523cc0837937d6d018fb3d8d49e4': '色',
                'a8cf98ca06a8c5bae63825a44a5903e3': '世', '9646d838f7324ed72ddef055a2cc14d7': '方',
                '800e481c648491e552e0d6e91082ea37': '寓', '5dd495431c41681acc49a304b3d567ed': '风',
                'd86662c816b536ca500a6c1c3d6282ae': '幼', '8a5ee99e561e0345d9e31e3debe7cfe6': '羊',
                '1f5cb46b9d020b136dc3bb69b3f1f1ff': '烫', '8dee1f8f7b8010c2de0d51a32f00b644': '来',
                '76ac6c213a71903f59dd0b093a5ec9b5': '髙', 'a488b220fbbe2a528f10b0fea79a0437': '厂',
                '88f1720d6753afc8c4027369da51e8d8': '兰', '4c1d9036578af51553e2afa0e72ae76a': '阿',
                '9115b73ec33ec3394f7f5b5b4d48b8ba': '贝', '6207a8ee95df77d9073fe354351f5e32': '皮',
                'cf6ade958b5347954da1ff7666d80064': '全', '637ff91efa4b44493736c2aab206b0a4': '女',
                '4ecfe11e3522a164b9ba9d4e3f4067e4': '拉', '5590c7618f45a5ed7a5309c55794badc': '成',
                '9b3b1b487d69738284da6f69a9aeffb2': '云', '3e020aaba65d1c918f66128334ba9781': '维',
                '85b99a275e1c6e5e6c19f69f322557ad': '贸', '1df55157a1493d49054d827de1743e45': '道',
                'e1f3631e8b49b210defd60f39d62a011': '术', '9ce6f73e12dd4773050cb13cc0db72de': '运',
                'f383b66f4a6f40d8025ca6ea8db744ea': '都', '2c6bdc31bd38490868f160c0f9079cc7': '口',
                '9079665cbd6ea61c81ee6e4c432e0bd2': '博', '3b534f75609d6359b0c1565e0ed29ae2': '河',
                '6cd5d623181671ab13c49cabeee63fa8': '瑞', 'f9ee7ac7ec0bf2c930f5ba921605046b': '宏',
                'ab61e8260806aa94937f9be8cd638988': '京', '880e14df3db89c9f52b571c3fce64d0d': '际',
                '3ca7661a825b6909f25d1c9f8cfe2172': '路', '7850d63cedb33c711fa772edf44fd8fe': '祥',
                '7d0b50b92b5f9948056ffcf965a63f05': '青', '018489733745b793bca0e0b5b1064786': '镇',
                '0771beefc78ccfd4fcebb430d49030d5': '厨', 'c9579aef2d38ae69b8db6de81fafdd9f': '培',
                'cf07712919196a04bd45792796a71bea': '力', '43eb5d71104a92da0f21e70070fd5482': '惠',
                'a1a93f9e003a6b451bad41ef48f34c6d': '连', '5250010a671e62c31abc4b0a018df476': '马',
                '41904886025d184df0962af0b76608f7': '鸿', '07c9ed64bee43c740f08fab032885baf': '钢',
                'd6663374b2a090733687d2bf2e5f2015': '训', 'e1b908628db058263433cf2c596c8e48': '影',
                'a41df76274e61dc2d34ce1c26fb2933c': '甲', '076f8af592e6bd518776633add7ada08': '助',
                'c6bc4c626b8e0764857b72cb8a5ead0a': '窗', '36767055d81d094959dc0cc6ab704011': '布',
                '622a21961b2c13c230ce711e93350f01': '富', '5d6a12b8bfc2153ee2dafae170b8d08b': '牌',
                '8f1cd8b32314db76c473a0162c0da989': '头', 'c935fdaf0f99451692a8bed25dd1fe15': '四',
                '57556c69e1e290f464e73c31c2e534a2': '多', 'ca1bdc9bc31fb04780737fd8b839aa68': '妆',
                '00d1fdc6272767907d41821bb7917260': '吉', '8bd5ad717df06793acff623c27fb0aaa': '苑',
                '7fa8557ff03d98450e1a9cf45c4e0f68': '沙', '301b4253784da48c15a38ea8c7b9db83': '恒',
                '89eb4dddc31ddf577d516aa30eeed115': '隆', '326d36f444d45fc08dad4257b95e2650': '春',
                'd86094d5be04832c5e8284a0ba3ea64e': '干', '2ab8dc6f9c8391bb4b03d2c5e10d0651': '饼',
                '357f65b7050e055a32ec50f3e369b289': '氏', 'ede6607004fb2c2871e01669ca04cacb': '里',
                'ac24589995e27c3ca58663c56654748a': '二', '774da9a964741f9c6ffd549acdc27f99': '管',
                '59b8b0b420c92cb2e5ebc41fb92c72f3': '诚', '3c45a92ddc2e297c715499cdf5c47935': '制',
                '5490722b28fd923910e6d9a7b85a1a6f': '售', '85027a9d3f968577478c1016e052ba31': '嘉',
                'fcc4f5dba9d95eddc9aba6f42a1a5095': '长', '715e603d974f8a7336a405803e8f6ec4': '轩',
                '1b5ff91cf537d057c91a62ac41b3dd69': '杂', '074c9b56498c8691eb25666d4ded7910': '副',
                '49e5ae0d9f691056a973c31db2a15792': '清', '9893b2bdf2326915bba94fe3f78fedae': '计',
                '12dbd08a423b9046b89d25b283a002fc': '黄', '6b72951f41287b929ddc3c6fd98f85eb': '讯',
                '40ebd8b5e99e5cba3574b7fb6294f454': '太', 'f6e7aed9a679f322d7dbf9183ef8c6fa': '鸭',
                'e02e682cd85419f82c6f1cd95f72e270': '号', '3a3d616bc0e425d0ac301ed70e9d4609': '街',
                '3cc34bcf08bf120a686448b1777ead87': '交', '130554f622622a37da1da1a090317b45': '与',
                'f348e7b8b21c25e7244acab3377a54d9': '叉', '579dff683e2a9d7e0a125edda36b09cd': '附',
                '70fc7428cd910f5eb49dd444648390bd': '近', 'ac06ceeba0ced8df0404705d8a99ad4f': '层',
                'd242c812f8dea21398536624b1d1b3ff': '旁', 'a8d55ca7af1c63744161567dbe27893e': '对',
                '748580c7d3c0f1dafca29f9d290fd76e': '巷', '7225dcf2b2fa859c679e85d19b4ea69e': '栋',
                '2e1e8fccd00392145e669c36cfcf9c15': '环', '463714793ecb070c5d1066473450861a': '省',
                '890c24228a5efc8f5a6d716e3aebe27b': '桥', '223b27c0c6ebe05a5503ce25f6c17085': '湖',
                '892511fc7a7e35ff904548df35016207': '段', '7d6f942a9024ec49fb778e862f49d719': '乡',
                'c0a759dbc808c9fee0119c55c8e90ae9': '厦', '30f699810803f7112e3c23c0a2bc2216': '府',
                '3938eb4e7629dcbbdcd6a37b6c1ca12e': '铺', '6df703a1240e951b60858497a14c9ae6': '內',
                'a1d7ef63b32e07b5566317f6826d2acd': '侧', '2e48a2674139328a9e2184d3bf09d4b1': '元',
                '54a26eff6186bbbeaf2f2097e05a72f3': '购', '48604a0672e3d5efb3eef7134486a41d': '前',
                '01509d02dfed9f03ad1ebfe3378ef106': '幢', '7ac2f482d3629b8e06ab373710ef9c12': '滨',
                '75945d17beaf51706a7b609aac77eb3b': '处', 'c26f13dda4ff45dca83738d8142cc2e2': '向',
                'afff0e26ca22752ee279ed956dbf9490': '座', 'baedbc61cbdc69664139ebef448c4257': '下',
                'a6cdd02445f84290c9e6bd48e4afe728': '県', 'f912ec906204318064b8dba325028483': '凤',
                '2be552dd917a978805b20c893c9ecf30': '港', '4e278369f97fe5f2f8ae363333e82aa0': '开',
                'b1a6dda40c2e8394c3c869a72e194473': '关', '3cd2820e9db4ac7ec106b5cd3fe92292': '景',
                '44fc3fd8a7b04e28743532aebd812012': '泉', '1cd2eec926907b4a1eaf0297bed5d0c8': '塘',
                '9697463234cf47900f0809b790c100cc': '放', 'adba73fd6573a06697fc461fb56e4ebb': '昌',
                'd9b595480cbd9c200758766f44ea653c': '线', 'de3aeb2f9e78580bd10bb42ad1558ec1': '湾',
                'f80d15cac8a6be960c2094437fbf68d2': '政', '0f84154d2c74043dbeb04f231fed904f': '步',
                '11266e80d4e47a5342b22a3675711a06': '宁', '9650e4b078283c10f5f5e64e2dc65747': '解',
                'e38079cda732102622d3a9ad5de522bf': '白', '78e017082b48f8089b90d1ef35419e51': '田',
                '8c923a0daf31d63b1bed0b304bf3e7d2': '町', '7f2c456081b3b832432e713b09ab701a': '溪',
                '081962f7eec22ac7efdd1f5a14fbcaf1': '十', '7b95ac75c00b400b4eb4dc53a038ca46': '八',
                '0c683499127c6546b2fb695c551f07de': '古', 'd4fc7e87209718efb3ff7e6ef8aa360d': '双',
                '7ea278c4b81f5bd7476d9347660c766e': '胜', 'e801e6d2ffa65a36cbcd1d12ae98b75a': '本',
                '600ea62b1da2d18098b24697744ff067': '单', '9b968de900c6e802a475e11577bd2e24': '同',
                'cbfa6758f44d111be7a446fa879b29eb': '九', 'ac3eabd221707017c848c66a77f6336e': '迎',
                '5c3ae9704251bd27deef5df1e80b183c': '第', 'd9692011030ea53fed7dd4a35a3114ef': '台',
                '48131acd93dc19c7e184bc5d443a371c': '玉', '08407bbcfc55e57d14f81d74c6c7d799': '锦',
                '24e173bd7fdd574845857869bede5501': '底', 'c2ae24ba52c0fec6296a1bd0353033be': '后',
                '869366f84fe0f503605d685acf288ee7': '七', 'bbe98f18d6e2092f32c939463adae93b': '斜',
                'a847eca2c1c78dd231a03b49d4d35c8d': '期', 'd7a8fe8f8bc343c1a85800e53906792a': '武',
                'ccc4491606a054d2d76eb5364bc16a85': '岭', '44b7786a5d7d64c089303f4eb1aa5aac': '松',
                'e5ee3966ed484d2a4dc9d16e3cd2c3ad': '角', '69b0d2490232acb94aec097341b4a322': '纪',
                'c83832828a2610d429352f332526bd80': '朝', 'f940fb5944edc1a7094395df6428a5ca': '峰',
                '30a0566febe9a8d21fcfee0c8eb7cefb': '六', '68fb8e6f5c986b0a8cb8ff3345a2e587': '振',
                'd0dc29da30af4e85fb077635e6b223ec': '珠', 'c1e2ed364e9ddfe673b937f9a0d9a86e': '局',
                '3b93403c666cc9d9a5d88c13df6595eb': '岗', '321fcafbc03aa8af5a2ef63f2f28d3d4': '洲',
                '6f93e44701fbee393909b884a3d7340f': '横', 'a307743ea988bb08f2b3295f60f17e34': '边',
                '3b8a8abf2a8297f9b6a18b31a2d97036': '济', '91d4e84f8d06769ca7819c063353a8de': '井',
                'b8e7d5fd802cffb478a44d634875c6b6': '办', '89c027ca2770222c9f4c04c0dba6cb90': '汉',
                'fdde428c38f17dd9b999a2cebff44960': '代', '04fe1d0d578a8d726557e524539cffd2': '临',
                '0e9adc3f5bff9bd59d301719cc033a1e': '弄', 'aaa9e365abe3fe36c73e5ffc05149b42': '团',
                '5a7843db954a425401a4c972c63cbfc2': '外', '1373dff8d68a50369116cd99a44ff3a6': '塔',
                '286213477b07429b954f659d340395f0': '杨', 'e531050a8981881f7bccfc70bfc0ccb8': '铁',
                '994351b770ba44dd7b9f800d9af07381': '浦', 'f3af32627ebb57283a317dddabae87ea': '字',
                'bdf57a54a9fdec47d47cedfc0b9fea5b': '年', 'c69fcbf54469f681d4f47cd227f0bb30': '岛',
                '860ba7f897bd5771bd38f36b77e63cc0': '陵', 'efa3601116da1b8301176ce424c790e3': '原',
                'ca05131398444f77f42c8e38ca527f08': '梅', '8cc005a19ae01816d58630e37962738e': '进',
                'c61eabc1a8ef9af9e3c74b5cc7748abf': '荣', 'd01aaee4b4e8d6e54ea15ba3fa9521fe': '友',
                'ec0afcbf16d075c303e4628598ac3c1b': '虹', 'd3ba27f2938d0d6aaa68ee9473ee0b89': '央',
                '77f525aeed078f388c73291443066140': '桂', 'cf4d897cab6b7a7e921d0507591433a2': '沿',
                'dfad5aee5f6b66d4941cb60a408e4881': '事', '73452563e80bb51a4c9351cd35471ccc': '津',
                '1bae273ec36f95cb9126fe5282623e7c': '凯', '232c58f834b1d0d049b20600c9042c2f': '莲',
                '581d38f52544c33231aa952098bfe1ec': '丁', '8545a7c32bb4ca3378b7206ce55b8c18': '秀',
                '9d9478377afbf367b7528a3cdfe6ee9c': '柳', 'f3083f3d8449644adf811ccc01c78807': '集',
                '9a2a4bcbf41a28e49b6957969f7a7f0c': '紫', 'c4923f452f36d6bc29f0392df4d77381': '旗',
                'a1e0681069a53e7b4c6e52296bff01bb': '张', '54a05accc27b6e545f5eb4ec00db4991': '谷',
                '334d05d1c06b97a6f6e47166941135d1': '的', '630330109649ddc5110380c3f98934cb': '是',
                'b6f88f92a3b13f4cf7bc9a8ddd4db25d': '不', 'a1a012ee1d1ceb57287c9ba69395b530': '了',
                '370aeb34e214643326a8b10a80c93f81': '很', '7d0af0173240c294a792ada64bd03692': '还',
                'd9770cc37ac1d0255cbf34b72da288d9': '个', 'd7ff56ff5e3b931d372f6b64c30a2432': '也',
                '0b2411c0fc52cbead6664fb71a1889c3': '这', 'a573cefba8f3c3473a14bc0436b3186a': '我',
                '6a1f9a40d8cd44e806e32f9ac688806a': '就', '1703b0610f90e744b4f9cd90e8b0503b': '在',
                '64c68ffe18122fee53bb2ffb0af0f4f6': '以', 'b4e3e58c72146448864755506112389f': '可',
                '384afb513c09236581b790c08e2629e0': '到', '7542adf5cd8c41af0cf509bca4f1b3b4': '错',
                'eee646ad3b37488c32ba0b8622f6efa7': '没', '400f841063330a64603df335a95b681b': '去',
                '1473fbac947950239f02a4f213447de5': '过', '7f211233ad76706e0ec3234a978b0e98': '感',
                '30171714807b0fda9088afcc79cf0adb': '次', '9a0a6599f2319751bdfe9ea2151b5928': '要',
                '0491dff63f2887a3b8add2d7d9675cc0': '比', 'dc2abfd2c8bfe1d24f0bf0eb9c79e310': '觉',
                '5507ee15989dcf2b260848ad936ac32a': '看', 'be0f4b0ce02962e83a2d73eb94f02c49': '得',
                'f007612424e04f0bb34067a90db9b71d': '说', '3f34a52316b10cecd93890472e12fd24': '常',
                '44240ce512ddaabf6d61f1013a093c93': '真', 'c5c4cd646593d8ef77d4f6e0846a7712': '们',
                '7d26ae4fae426dbe372ab8ac4f10b9f5': '但', '1402410678215d0f4d210cbbffd631c8': '最',
                'e37077606bd02f3e8789fc3e9562471a': '喜', '6bec86f98299c1ba83bbdf3e8c9c8a0d': '哈',
                '8e96fc795028f8f32bae864f0066117b': '么', '8bb066739213eafb1966e51d20e95beb': '别',
                '7f32faee13aeb0d0ea6bb45284e64e23': '位', 'bad1b18643425ae77bb94d18ab078f51': '能',
                '71d486e08e4397da67fbba0abf724255': '较', '09e79e0b7181d60d3846b653c665915f': '境',
                '4da112ea0593d818def15ff9e40a38fe': '非', '3da4bbe1b812708f791d011b87c20c7d': '为',
                '5b54f3df954bfe740e22ef588fd95dd4': '欢', '8440d243ab4aa07a892d1276a68837cd': '然',
                '0cde7f635eda249eb38c7a0eeac1e52b': '他', 'bfc4c30eca12548fea98072fd35c40d6': '挺',
                '32a81378881d0b9b4fd91eecca31df89': '着', 'acf1fd25a300df6c6a255bb352aae408': '价',
                '757a58be3af05d51ed41c8a6fa91ae33': '那', '68ab6705fc1fb75f90aec37924f0d0e1': '意',
                '4ecc2529325fa7265bbd6d487690f3b0': '种', 'c61259fefe0d24a3496c2dfb45bebb98': '想',
                '386fe27ff455c40a3dd771be23d62e1a': '岀', '02b0b451f18c4f1324adceef6091bc47': '员',
                '1c210a50d5f554c1e4fc30cc43fa7655': '两', 'b0c66ebb575919882beab10543c3ec87': '推',
                'ed8fff408ca1323774ed5285af7b851e': '做', '20059dee5dc7e7583e9573c5d239c66f': '排',
                '69f0174fbd9b3a77d2f6128d5846a8c1': '实', 'be202b8724288b3b4b5b1f287a3e3a0a': '分',
                '14d150154e5c851ef299cf810ea3a06e': '间', '0472fc9fe5099732149cb71648195881': '甜',
                'df40c8350ec1e13e0f622a22f583f046': '度', 'eaa57f368ddb7f7731cabe209b7e8f3c': '起',
                '5f5582950a0a6d8c8747273a75ceb2f5': '满', '5a1685097a8905675a71e59c68cacf3e': '给',
                'b9f19977470272b434e4ed58f0298618': '热', 'a5f337ec6b9701d09d910c3d3f2f620b': '完',
                'e59a58cd19ae059d698fe268eb195dd2': '格', 'f63685208a87aeef7ed0ca90625e5069': '荐',
                '431b09746cbe4fb82d3cf3d63cbba041': '喝', '0b6db4e319ceb6439ffda9a93da9d744': '等',
                '6c74fff7944334c30da04c865afbc8f0': '其', '5392528ade9bc30239d01daf91c75227': '再',
                '774b14b593ffeff45ef0e2776313ba19': '几', '0dabe6a26a75ed0a3a4c769a8efe9465': '只',
                'f088b3d381873712be0a5b0b17f4ed04': '现', 'c9219de5aa5f1c9686b555d2d41cd24f': '眀',
                'e92ca8a31870fe791337aea45f54c648': '候', 'f2f269a24fa3fbec9ec18a6704767050': '样',
                'f28028d96b773bb09f2cbfae8f08ce0d': '直', 'e96a99f4f2d9d741e4af83506d935335': '而',
                'f5dc50e04a2945239b41ad639907466c': '买', 'b562208a8264967dee236bc2d1050040': '于',
                '9bbbcc1bace4d4503d0f5dbd7213bb51': '般', '368a2315aee648f98c462d9f062be285': '豆',
                '4afe70189dbb13b6564cf8181578a197': '量', 'f0a94e011fa782d812c9b0d74974d106': '选',
                '1a2dfb77d8638375628fbc5d58252e93': '奶', '8c19a9c24e13fdc54ee23acdd25477f4': '圢',
                '26b3ab6430a1c83052dff42699d6114f': '每', '53c071bd49d982328d0a57bade683ffb': '评',
                'a546ac914af733c90a6ef2710679d727': '少', '9c35a8ad7ec94a4cb7221654b7a30e51': '算',
                '2ff2f4b39aad1bf9f302c0c04c233ec8': '又', '742e91c64d8d9818daa2acaeac5c62f9': '因',
                'a6d0eaa62f52dcae2c83c3518af0c684': '情', '93c4566c1167479474a27834c791a97f': '找',
                '985ef802057455183b153db572ce9ef7': '些', '261bad2b41af694917f6fe5ddb3736d3': '份',
                '4646bb0c424f5de368f07590bff0cdaa': '置', '9bd9c79fbe83bf1ebd379315a43dedc0': '适',
                '0a90fe7575aa46c58d5e9293ff052b15': '什', 'a1e339dc28ce3dbc9ff216e55ebae3b0': '蛋',
                '9ee3008c57e4f5b1d82a57d485395cd6': '师', 'b7cee40fe088492417e1958b0d4f644c': '气',
                '43f2f93829cc315f268cf5e6d530c362': '你', 'df1825c004b6f5a24a1cc6bbb3eb167b': '姐',
                '25368bd71a0774fe8ff252c04c439eae': '棒', 'f9f7ee013fb0fbd572732f7d6f6711d6': '试',
                'fbcf7c71e319473c3f49103923ae929e': '总', 'b6a1a0461f72ca5b6fd09a7874bc6422': '定',
                '063c4e48e5abc8bbbae0fd498860d705': '啊', '4128d206b501086a718010582866846d': '足',
                'cced7ab6ab53625a8c48610397d21295': '级', '646cf0e15e8cc6f45e7e7a5d9252c213': '整',
                '538d08ea81a09de47b9789561bcee379': '带', 'dad33daa0c59209823e9d731164e4b70': '虾',
                'd737900acaf0f3416575960cf22e137e': '如', '573aa1eb82a6aa70367290dcda4d78f0': '态',
                '7190c29b55dc9ed14fd24b11240fe696': '且', 'fb0439e38bcb0a330c6b92959357da36': '尝',
                '5fb376adef922941efdb939152e8904d': '主', '44fa489f49f0b00ea6ba9353fcb6cbdb': '话',
                '5ac40ceb33859d2d71d6a29b23b083cb': '强', '93754ad5dc50cda677df44173b9afbdb': '当',
                '8232b7d3156ceb46eac5c7709433310d': '更', '449444b86d7b828bf63d07330f2e9970': '板',
                '81a1d294fc74fde1ed012732dc428c42': '知', 'bec71d6ded10da6106b5f839bd26753f': '己',
                'fddcd971393d3049bf5ebda81ff81a2e': '无', '84a0bc2c594f02a78b351b6b29f76079': '酸',
                '623932365e9f973c4d521e3a08a98aab': '让', 'cc7bc1491d2f4608ee4a1f95b4c3d243': '入',
                '91dcb6814aa2e5ec5c9c282ffe9253b4': '啦', '331becbbc50fb89a1e6d11c83917ec56': '式',
                '71e8865077b34afd1203dff6180ce7cd': '笑', 'bd3d1ab8240b17decb8a02dbefda102b': '赞',
                '63de3482f19ac54f345078c4c8f41cb0': '片', '49e3c75c6196b68c17645d0f869d3f94': '酱',
                'aeb6b576ece16d181662bfa28124e63c': '差', 'f7fbca510ef9c7d027f99526d7ec67a0': '像',
                '876e2d9d255263acaeac9a5aad15383d': '提', 'ec5a2ddcfb2810519c8996d889b21dfa': '队',
                '67420364aecedc6964adbea12c13bf78': '走', '09bb20dc85efa46bfba2552b27eb15aa': '嫩',
                '7da4de602c14caec157b604de5fc141e': '才', '0d46e30fc1cf6e18df8d560da63f6bfe': '刚',
                '85ae7aa518ea82c1cb6a350564a5820a': '午', '7d1704bf5ce444c3a192885cb2b1dd38': '接',
                '421cfdf3e711c78376b0a77c64c93b4e': '重', '98d56a7b1365e20a4e7e007549cca244': '串',
                '2f128c2c8296f87773957863776336f9': '回', 'f9a0536cf902b4fbabb7ff757e24dec7': '晩',
                'd6988a53728b959e96eee351dcafd7eb': '微', '73d021cc07422aa1ed92335dec5476d0': '周',
                '4a9f74350d4cbc50df149338c31c24e5': '值', 'c53eac81ae3cdb33f436c5a2514e802b': '费',
                '35a0fe027bc78673ec7ecc34677000d8': '性', '654155abd969b1e04ab47ee559602c48': '桌',
                'fc20a0988821eba88c9004ea779c9e7d': '拍', '45238eb780ad1c91297c08a19bdea701': '跟',
                '9ff352ce30fa673d0d761f342aaf084a': '块', 'a829e39fb6e5c6105eba3af78680692e': '调',
                '237441978978aba8543af3bd19bdba87': '糕'}

    # print(names)
    # print(md5_l)
"""
