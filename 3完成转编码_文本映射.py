from bs4 import BeautifulSoup
import re
import hashlib
from config import *
md5_dict = md5_dict
words = words.replace('\n', '').replace(' ', '')

with open('./dianping2.xml', 'r', encoding='utf-8')as f:
    t = f.read()
md5_list = {}
soup = BeautifulSoup(t, 'xml')
ttg_list = soup.find_all('TTGlyph')
for ttg in ttg_list:
    tar = re.findall(r'name=".*?"', str(ttg))[0]
    name = re.findall(r'name="(.*?)"', str(ttg))[0]
    result = str(ttg).replace(tar, '')
    md5_code = hashlib.md5(result.encode(encoding='utf-8')).hexdigest()
    #
    # args = (md5_code,)
    # cursor.execute(sql, args)
    try:
        result = md5_dict[md5_code]
        word = result
        # md5_list[name.replace('uni', '@@@').encode('utf-8').decode('unicode-escape')] = word
        md5_list[name.replace('uni', '&#x').encode('utf-8').decode('unicode-escape')] = word
    except:
        print("MD5字型：文本字典错误")

print(md5_list)
print(len(md5_list))
