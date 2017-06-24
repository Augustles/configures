# coding=utf-8

# 命令行启动
#  jupyter notebook
#  jupyter notebook --no-browser
#  jupyter notebook --port 9999
#  jupyter notebook --help
#  jupyter notebook --ip=0.0.0.0 #外部访问
#  jupyter notebook --no-browser --port 8888 --ip=0.0.0.0
c.NotebookApp.ip='*'
c.NotebookApp.open_browser = False
c.NotebookApp.port =8888
c.NotebookApp.password = u'sha1:1462c4246120:d466de830658e756be8ad408bcefd20397453282'
