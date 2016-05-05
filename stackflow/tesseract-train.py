# coding=utf-8

import requests
from time import sleep
import os
import pytesseract
from PIL import Image, ImageEnhance


os.chdir('/home/august/work/51yyto')


def vcode(fn):
    im = Image.open(fn)
    # 训练lang可以提高识别率
    code = pytesseract.image_to_string(im, lang='51', config='-psm 7')
    nfn = code + '.png'
    os.rename(fn, nfn)
# for x in os.listdir('.'):
#     print x
#     if x.endswith('.png'):
#         vcode(x)

# Tesseract-ocr 训练

url = 'http://www.51yyto.com/index.php/api/checkcode/image/80_27/1461569694221'
def d(url, i):
    r = requests.get(url)
    with open(i, 'wb') as f:
        f.write(r.content)

for i, x in enumerate(range(200)):
    fn = '00' + str(x) + '.png'
    print(fn)
    sleep(0.75)
    d(url, fn)
    print('start to vcode')
    vcode(fn)

# 训练步骤
# 1. 转化为tif格式
for x in os.listdir('.'):
    cmd = 'convert {0} -flatten -monochrome {1}.tif'.format(x, x[:-4])
    os.system(cmd)

# 2. 合并tif
cmd = 'tiffcp -c none *.tif target.tif'
# os.system(cmd)
# 3. 重命名
os.system('mv target.tif code.font.exp0.tif')
# 4. 生成box文件
cmd = 'tesseract -psm 8 code.font.exp0.tif code.font.exp0 batch.nochop makebox'
# os.system(cmd)
# 5. 调整识别结果 jTessBoxEditor打开box文件, 对默认识别结果调整
# 6. 从box文本中训练样本, 特征文件, 生成tr文件
cmd = 'tesseract -psm 8 code.font.exp0.tif code.font.exp0 box.train'
# os.system(cmd)
# ubuntu12.04, ubuntu14.04默认没有装training tools
# 聚集, 产生文字的原型
cmd = 'shapeclustering -F font_properties -U unicharset  *.tr'
cmd = 'mftraining -F font_properties -U unicharset -O banker.unicharset *.tr'
cmd = 'cntraining *.tr'
# 重命名
'mv unicharset 51.unicharset'
'mv shapetable 51.shapetable'
'mv inttemp 51.inttemp'
'mv pffmtable 51.pffmtable'
'mv normproto 51.normproto'
# 生成语言文件
cmd = 'combine_tessdata 51.'
