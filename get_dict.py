# 获取当天的字体映射关系，下载4份woff文件，然后处理成4份字典，保存在pkl文件中供使用
import requests
from bs4 import BeautifulSoup
import re
from fontTools.ttLib import TTFont
import hashlib
import pickle
from config import *


md5_dict = md5_dict
words = words.replace('\n', '').replace(' ', '')


def download_css(svg_css_url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 's3plus.meituan.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    r = requests.get(svg_css_url, headers)
    fonts = re.findall('//s3plus\.meituan\.net/v1/mss_.{1,50}/font/.{1,20}\.woff', r.text)
    tag_class = re.findall('} \.(.*?){', r.text)
    d = {}
    if len(fonts) == len(tag_class):
        for u, t in zip(fonts, tag_class):
            d[t] = 'http:' + u
    return d


def build_dict(d):
    tag_dict = {}
    # 对d循环取出woff的url
    for k in d.keys():
        url = d[k]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        r = requests.get(url, headers=headers)
        woff_file_name = k + '_' + url.split('/')[-1].replace('.woff', '')
        # 下载woff文件
        with open('./font_files/' + woff_file_name + '.woff', 'wb')as f:
            f.write(r.content)
        print(woff_file_name, '下载完成')
        # 把woff文件保存成xml文件
        font = TTFont('./font_files/' + woff_file_name + '.woff')
        font.saveXML('./font_files/' + woff_file_name + '.xml')
        # 读取xml文件，读取TTGlyph的字型和name用于映射
        with open('./font_files/' + woff_file_name + '.xml', 'r', encoding='utf-8')as f:
            t = f.read()
        md5_list = {}
        soup = BeautifulSoup(t, 'xml')
        ttg_list = soup.find_all('TTGlyph')
        for ttg in ttg_list:
            tar = re.findall(r'name=".*?"', str(ttg))[0]
            name = re.findall(r'name="(.*?)"', str(ttg))[0]
            result = str(ttg).replace(tar, '')
            md5_code = hashlib.md5(result.encode(encoding='utf-8')).hexdigest()
            try:
                result = md5_dict[md5_code]
                word = result
                md5_list[name.replace('uni', '@@@').encode('utf-8').decode('unicode-escape')] = word
                # md5_list[name.replace('uni', '&#x').encode('utf-8').decode('unicode-escape')] = word
            except:
                print("MD5字型：文本字典错误")
        tag_dict[k] = md5_list
        # break
    return tag_dict


def get_dict(url, headers):
    r = requests.get(url, headers=headers)
    page_source = r.text
    # print(page_source)
    # 访问含有woff文件信息的css链接,得到woff文件的分类和url
    svg_css_url = 'http:' + re.findall('//s3plus.meituan.net/.*?/svgtextcss/.*?css', page_source)[0]
    # 下载woff文件
    d = download_css(svg_css_url)
    print(d)
    # d{'address': 'http://s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/2e01b109.woff',
    #  'shopNum': 'http://s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/6360abca.woff',
    #  'tagName': 'http://s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/bfec2e8f.woff',
    #  'reviewTag': 'http://s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/2e01b109.woff'}

    # 下载、解析woff文件，生成当天的编码-文本映射字典
    tag_dict = build_dict(d)
    print(tag_dict)

    data = pickle.dumps(tag_dict)
    with open('./dict/dict.pkl', 'wb')as f:
        f.write(data)
    print('字典已经生成')


if __name__ == '__main__':
    # 随便访问一个页面下载我woff文件
    # url = 'http://www.dianping.com/nanping/ch10'
    url = 'http://www.dianping.com/shop/G2mjXn2a0usmVBN5'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    get_dict(url, headers)

