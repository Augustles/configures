####jupyter安装
pip install jupyter
####jupyter配置
####生成jupyter_notebook_config.py
jupyter notebook --generate-config
具体配置在conf/jupyter_notebook_config.py
####支持go jupyter
####https://github.com/gopherdata/gophernotes
docker pull dwhitena/gophernotes:latest
docker run --name gophernotes --net host -d dwhitena/gophernotes:latest
docker run -p 8888:8888 -d dwhitena/gophernotes jupyter notebook --no-browser --ip=0.0.0.0
####使用
shift+enter运行cell
