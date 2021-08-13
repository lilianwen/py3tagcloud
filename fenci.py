import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser

from pytagcloud import create_tag_image, make_tags
import re
import time
from collections import Counter
import datetime

USAGE = "usage:    python extract_tags_with_weight.py [file name] -k [top k] -w [with weight=1 or 0]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
parser.add_option("-w", dest="withWeight")
opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]

if opt.topK is None:
    topK = 10
else:
    topK = int(opt.topK)

if opt.withWeight is None:
    withWeight = False
else:
    if int(opt.withWeight) is 1:
        withWeight = True
    else:
        withWeight = False

content = open(file_name, 'rb').read()

tags = jieba.analyse.extract_tags(content, topK=topK, withWeight=withWeight)

counts=[]
word_freq = {}
if withWeight is True:
    for tag in tags:
        print("tag: %s\t\t weight: %f" % (tag[0],tag[1]))
        word_freq[tag[0]] = int(tag[1]*1000)
        print(word_freq)
        counts.append(tuple(word_freq))
else:
    print(",".join(tags))
#if withWeight is True:
#    for tag in tags:
#        word_freq = []
#        print("tag: %s\t\t weight: %f" % (tag[0],tag[1]))
#        word_freq.append(tag[0])
#        word_freq.append(int(tag[1]*100))
#        print(word_freq)
#        counts.append(tuple(word_freq))
#else:
#    print(",".join(tags))
counts = Counter(word_freq).items()
print(counts)
#counts = (counts,)
#print(counts)
#counts = ([('老公', 34), ('触发', 12), ('她家', 9), ('婆婆', 9), ('每天', 8), ('直到', 8), ('失眠症', 8), ('结婚', 7), ('非常', 7), ('饼干', 7)])

# 打印的语言
languages = input("选择打印英文按0，打印中文请按1，打印中英结合请按2（默认打印中英结合）：")
language = 'MicrosoftYaHei'
try:
    if languages == "0":
        language = 'Lobster'
    elif languages == "1":
        language = 'MicrosoftYaHei'
    elif languages == "2":
        language = 'MicrosoftYaHei'
except:
    language = 'MicrosoftYaHei'

# 打印的字体大小
fontszs = input("选择特大字体请按0，大字体请按1，中字体请按2，小字体请按3（默认大字体）：")
fontsz = 90
try:
    if fontszs == "0":
        fontsz = 180
    elif fontszs == "1":
        fontsz = 120
    elif fontszs == "2":
        fontsz = 90
    elif fontszs == "3":
        fontsz = 60
except:
    fontsz = 120

# 图片长宽
imglength = 1000
imgwidth = 800
try:
    imglengths = int(input("请输入图片长（默认1000）："))
    if isinstance(imglengths, int) == True:
        imglength = imglengths
except:
    imglength = 1000
try:
    imgwidths = int(input("请输入图片宽（默认800）："))
    if isinstance(imgwidths, int) == True:
        imgwidth = imgwidths
except:
    imgwidth = 800

# 背景颜色
rcolor = 255
gcolor = 255
bcolor = 255
print("RGB颜色对照值可以参考博客：http://www.cnblogs.com/TTyb/p/5849249.html")
try:
    rcolors = int(input("请输入背景颜色RGB格式的R（0-255默认白色）："))
    if isinstance(rcolors, int) == True:
        rcolor = rcolors
except:
    rcolor = 255
try:
    gcolors = int(input("请输入背景颜色RGB格式的G（0-255默认白色）："))
    if isinstance(gcolors, int) == True:
        gcolor = gcolors
except:
    gcolor = 255
try:
    bcolors = int(input("请输入背景颜色RGB格式的B（0-255默认白色）："))
    if isinstance(bcolors, int) == True:
        bcolor = bcolors
except:
    bcolor = 255
        
# 用一个时间来命名
nowtime=time.strftime('%Y%H%M%S', time.localtime())
# 设置字体大小
tags = make_tags(counts, maxsize=int(fontsz))
# 生成图片
create_tag_image(tags, './tagcloud/' + str(nowtime) + '.png', size=(imglength, imgwidth), fontname=language,background=(int(rcolor), int(gcolor), int(bcolor)))
print(('已经储存至./tagcloud/' + str(nowtime) + '.png'))