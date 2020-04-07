import json
import random
import requests
import pickle
from lxml import etree


def get_reviews(html):
    reviews_temps = html.xpath("//span[@id='reviewCount']//text()")
    # print(reviews_temps)
    reviews_temp = ''
    for i in reviews_temps:
        try:
            j = i[1:-1]
            # print(j)
            reviews_temp = reviews_temp + num_dict[j]
        except:
            reviews_temp = reviews_temp + i.replace(' ', '')

    return reviews_temp

def get_good_reviews(html, reviews):
    good_reviews_temps = html.xpath("//label[@class='filter-item J-filter-good']/span/text()")
    if len(good_reviews_temps) >=1:
        good_reviews_temp = int(good_reviews_temps[0][1:-1])
    else:
        good_reviews_temp = ''
    # print(good_reviews_temps)
    # good_reviews_temp = ''
    # for i in good_reviews_temps:
    #     try:
    #         j = i[1:-1]
    #         print(j)
    #         good_reviews_temp = good_reviews_temp + num_dict[j]
    #     except:
    #         good_reviews_temp = good_reviews_temp + i.replace(' ', '')
    return good_reviews_temp

def get_price(html):
    price_temps = html.xpath("//span[@id='avgPriceTitle']//text()")
    # print(price_temps)
    price_temp = ''
    for i in price_temps:
        try:
            j = i[1:-1]
            # print(j)
            price_temp = price_temp + num_dict[j]
        except:
            price_temp = price_temp + i.replace(' ', '')
    return price_temp


def get_place(html):
    place_temps = html.xpath("//span[@id='address']//text()")
    # print(place_temps)
    place_temp = ''
    for i in place_temps:
        try:
            j = i[1:-1]
            # print(j)
            if j in address_dict.keys():
                place_temp = place_temp + address_dict[j]
            else:
                place_temp = place_temp + num_dict[j]
        except:
            place_temp = place_temp + i.replace(' ', '')

    return place_temp

def get_manage_time(html):
    manage_time_temps = html.xpath("//div[@class='other J-other Hide']//span[@class='item']//text()")
    # print(manage_time_temps)
    manage_time_temp = ''
    for i in manage_time_temps:
        try:
            j = i[1:-1]
            # print(j)
            if j in shopdesc_dict.keys():
                manage_time_temp = manage_time_temp + shopdesc_dict[j]
            else:
                manage_time_temp = manage_time_temp + hours_dict[j]
        except:
            manage_time_temp = manage_time_temp + i.replace(' ', '')

    return manage_time_temp

def get_name(html):
    names_temp = html.xpath("//h1[@class='shop-name']/text()[1]")
    name_temp = "".join(names_temp)
    return name_temp


def get_shopinfo(url, proxies):
    # url = "http://www.dianping.com/shop/98250909"
    # time_temp = random.randint(10, 25)
    # time.sleep(time_temp)
    for i in range(1, 10):
        try:
            res = requests.get(url=url, headers=headers, proxies=proxies, timeout=8)
            res.encoding = 'utf-8'
            page_source = res.text.replace('&#x', ';@@@')
            # print(page_source)
            html = etree.HTML(page_source)
            # 使用xpath解析源码得到数据
            # 餐厅点评数排名榜
            reviews = get_reviews(html)
            # print("点评数:" + reviews)
            # 餐厅好评数排名榜
            good_reviews = get_good_reviews(html, reviews)
            # print('好评数:' + str(good_reviews))
            # # 餐厅价格排名榜
            price = get_price(html)
            # print('价格:' + price)
            # # 输出餐厅分布势力图
            place = get_place(html)
            # print('地址:' + place)
            # # 夜间餐厅热力图（22:00后继续经营）
            manage_time = get_manage_time(html)
            # print('经营时间:' + manage_time)
            # # 餐厅名
            name = get_name(html)
            # print('餐厅名字:' + name)
            shopinfo_temp = {}
            shopinfo_temp["reviews"] = reviews
            shopinfo_temp["good_reviews"] = good_reviews
            shopinfo_temp["price"] = price
            shopinfo_temp["place"] = place
            shopinfo_temp["manage_time"] = manage_time
            shopinfo_temp["name"] = name
            shopinfo_temp["shop_url"] = url
            if name:
                shopinfos.append(shopinfo_temp)
                print(shopinfo_temp)
                break
        except:
            print('店铺详情页请求出错')
        else:
            proxies = get_proxy_ip(orderid, 1)


def get_shopls(start_url, proxies):
    # 区域内的一个服务分类
    shop_urls = ''
    url = ''
    html = ''
    # 重试10次
    for i in range(1, 10):
        url = start_url

        global headers
        try:
            res = requests.get(url=url, headers=headers, proxies=proxies, timeout=8)
            html = etree.HTML(res.text)
            shop_urls = html.xpath("//div[@class='tit']//a[@data-hippo-type='shop']/@href")
            for shop_url in shop_urls:
                headers['Referer'] = url
                headers['User-Agent'] = random.choice(ua_ls)
                get_shopinfo(shop_url, proxies)
            if len(shop_urls) >= 1:
                break
        except:
            print('店铺列表请求出错')
        else:
            proxies = get_proxy_ip(orderid, 1)

    next_urls = html.xpath("//a[@class='next']/@href")

    # time_temp = random.randint(10, 25)
    # time.sleep(time_temp)
    global flage
    flage += 1
    print(next_urls)
    print(flage)
    # print(len(next_urls))
    if len(next_urls) >= 1 and flage <= 20:
        headers['Referer'] = url
        headers['User-Agent'] = random.choice(ua_ls)
        next_url = next_urls[0]
        get_shopls(next_url, proxies)

# 快代理
orderid = ""
username = ""
password = ""
# 获取代理ip函数
def get_proxy_ip(id, ip_num):
    api_url = "https://dps.kdlapi.com/api/getdps/?orderid={}&num={}&pt=1&format=json&sep=1".format(id, ip_num)
    proxy_ips = requests.get(api_url).json()['data']['proxy_list']
    proxy_ips_dict = {ips: 0 for ips in proxy_ips}
    proxy = random.choice(list(proxy_ips_dict.keys()))
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                        'proxy': proxy},
        "https": "https://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                          'proxy': proxy}
    }
    return proxies


if __name__ == '__main__':
    # 代理
    # 获取存在pkl中的编码-文本字体映射关系
    with open('./dict/dict.pkl', 'rb')as f:
        tag_dict = pickle.loads(f.read())
    with open('./utils/ua.log', 'r', encoding='utf-8') as f:
        ua_ls = f.read().split('\n')
    # print(tag_dict)
    num_dict = tag_dict['num']
    address_dict = tag_dict['address']
    shopdesc_dict = tag_dict['shopdesc']
    hours_dict = tag_dict['hours']
    shopinfos = []
    flage = 0
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        'Referer': 'http://www.dianping.com/shenzhen/',
        # "Cookie": "s_ViewType=10; _lxsdk_cuid=1713499ce02c8-0dcbc25bb9338d-55123811-13c680-1713499ce02c8; _lxsdk=1713499ce02c8-0dcbc25bb9338d-55123811-13c680-1713499ce02c8; _hc.v=8c86e68e-d1bb-b6de-0426-348a6c567e47.1585725428; cy=7; cye=shenzhen; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=17138878d5a-b2-4b5-c33%7C%7C42",
        "Host": "www.dianping.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(ua_ls)
    }
    start_url = 'http://www.dianping.com/shenzhen/ch10/r3155d500'
    proxies = get_proxy_ip(orderid, 1)
    get_shopls(start_url, proxies)
    with open('test.json', 'w') as f:
        json.dump(shopinfos, f)
    print(shopinfos)




# http://www.dianping.com/ajax/json/shopDynamic/shopAside?
# 经纬度