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
####sudo 免密码
    %sudo   ALL=(ALL:ALL) ALL
    august ALL=(ALL) NOPASSWD: ALL
####python dict,list显示中文
    json.dumps(lst, ensure_ascii=False)
