####gitlab安装
    curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh | sudo bash
    sudo yum install gitlab-ce

####sentry 安装
    mkvirtualenv sentry
    pip install sentry
    sentry init # 初始化, 生成配置文件, 默认在~/.sentry目录
    sentry upgrade # 生成初始数据, 可以使用mysql数据库或者postgresql

    createuser nana # 创建管理员用户
    sentry run worker # 启动sentry服务, 注意启动顺序
    sentry run cron
    sentry run web # 运行sentry web界面

####邮件无法发送被ban(554错误)

####注意点
    注意开启邮件提醒
    设置SENTRY_DSN变量

