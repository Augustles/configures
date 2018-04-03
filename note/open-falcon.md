##open-falcon

1. [Open-Falcon官方文档](https://book.open-falcon.org/zh_0_2/quick_install/)
2. [open-falcon(v0.2)部署个人总结](https://www.jianshu.com/p/3df8e722359d)

####安装完golang,安装open-falcon
cd $GOPATH/src/github.com/open-falcon/falcon-plus/
git clone https://github.com/open-falcon/falcon-plus.git
make all
make pack
export FALCON_HOME=/opt
export WORKSPACE=$FALCON_HOME/open-falcon
mkdir -p $WORKSPACE
tar -xzvf open-falcon-v0.2.1.tar.gz -C $WORKSPACE

####启动falcon
./open-falcon start/stop
./open-falcon check

####安装dashboard
cd $WORKSPACE
git clone https://github.com/open-falcon/dashboard.git
cd $WORKSPACE/dashboard/
virtualenv ./env
./env/bin/pip install -r pip_requirements.txt -i https://pypi.douban.com/simple

#####配置文件
rrd/config.py

####启动dashboard
./control start/stop
./control status

#####plugins插件运行,修改配置,开启插件/修改目录
vim agent/cfg.json
    "plugin": {
        "enabled": true,
        "dir": "./plugins",
        "git": "https://github.com/open-falcon/plugin.git",
        "logs": "./logs"
    },

##### 修改插件执行权限,查看日志

```
chmod a+x agent/plugins/check_host/60_check_host.py

tail -f agent/logs/agent.log
```



####插件运行需配置,templates(报警规则),hosts(主机名),plugins(插件执行目录)
