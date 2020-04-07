from fontTools.ttLib import TTFont
font = TTFont('dianping2.woff')
font.saveXML('dianping2.xml')


# 加载出来之后观察两个文件的文字构造（1.顺序出发，2.字形出发）， 找出映射结果
