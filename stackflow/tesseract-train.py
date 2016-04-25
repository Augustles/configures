# coding=utf-8

import requests
from time import sleep
import os

# Tesseract-ocr 训练
os.chdir('/home/august/work/51yyto')
url = 'http://www.51yyto.com/index.php/api/checkcode/image/80_27/1461569694221'
# def d(url, i):
#     r = requests.get(url)
#     with open(i, 'wb') as f:
#         f.write(r.content)

# for i, x in enumerate(range(50)):
#     fn = '00' + str(x) + '.png'
#     sleep(5)
#     print(fn)
#     d(url, fn)


# 1. 转化为tif格式
# for x in os.listdir('.'):
#     cmd = 'convert {0} -flatten -monochrome {1}.tif'.format(x, x[:-4])
#     os.system(cmd)

# 2. 合并tif
cmd = 'tiffcp -c none *.tif target.tif'
os.system(cmd)
# 3. 重命名
os.system('mv target.tif code.font.exp0.tif')
# 4. 生成box文件
cmd = 'tesseract -psm 7 code.font.exp0.tif code.font.exp0 batch.nochop makebox'
os.system(cmd)
# 5. 调整识别结果 jTessBoxEditor打开box文件, 对默认识别结果调整
# 6. 从box文本中训练样本
cmd = 'tesseract -psm 7 code.font.exp0.tif code.font.exp0 box.train'
