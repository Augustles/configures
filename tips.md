#tips
####hosts文件屏蔽域名加快浏览器加载速度
`stackoverflow`

    127.0.0.1 www.google-analytics.com
    127.0.0.1 ajax.googleapis.com
    127.0.0.1 www.google.com
####防火墙
    iptables
    firewalld
    SELINUX
####生成公钥, git不用密码登陆, linux把生成的id_rsa.pub放入authorized_keys中
    ssh-keygen -t rsa -C
#####免密码登录
     配置.ssh/config
    ssh-copy-id -i ~/.ssh/id_rsa.pub august@127.0.0.1 -p 2225
####添加环境变量
    export PATH="/usr/local/python3/bin/:$PATH"
####服务器按照上传,下载
    sudo yum install lrzsz -y
####centos代码显示高亮
    git config --global color.ui true
####sudo 免密码
    %sudo   ALL=(ALL:ALL) ALL
    august ALL=(ALL) NOPASSWD: ALL
####python dict,list显示中文
    json.dumps(lst, ensure_ascii=False)
####更换git 地址
    git remote rm origin
    git remote add origin [url]
