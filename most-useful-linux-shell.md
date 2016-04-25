#牛逼的linux shell

####执行上条命令
	sudo !!
####http方式共享当前目录下文件
	python -m SimpleHTTPServer
####普通用户保存root文件
	:x !sudo tee %
####切换回上一个目录
	cd -
####切换到home目录
	cd ~
####替换上一条命令
	cat file.txt
	^cat^vi
####快速备份一个文件
	cp file{,.bak}
####免密码ssh登录主机
	ssh-copy-id remote-machine
####抓取linux桌面视频
	ffmpeg -f x11grab -s wxga -r 25 -i :0.0 -sameq /tmp/out.mpg
####清空或创建一个文件
	:>file.txt
####用ssh创建端口转发通道
	ssh -N -L2001:remotehost:80 user@somemachine
####重置终端
	reset
####在午夜的时候执行某命令
	echo cmd | at midnight
####添加可执行权限
    chmod a+x file.sh / chmod 777 file.sh
####远程传送麦克风语音
    dd if=/dev/dsp | ssh username@host dd of=/dev/dsp
####映射一个内存目录
    mount -t tmpfs -o size=1024m tmpfs /mnt/ram
####用diff对比远程文件跟本地文件
    ssh user@host cat /path/to/remotefile | diff /path/to/localfile -
####查看系统中占用端口的进程
    netstat -tulnp
####更友好的显示当前挂载的文件系统
    mount |column -t

####远程复制
    scp /home/adminuser/landing.gz leon@69.61.83.181:/home/leon
    scp -r /home/adminuser/landing/ leon@69.61.83.181:/home/leon/landing/ # 复制文件夹
####rsync(建议使用)
    rsync -avzP --progress  -r -e ssh /home/adminuser/landing root@69.61.83.187:/root/land
####测试磁盘读写速度
    dd bs=1M count=128 if=/dev/zero of=./largefile conv=fdatasync
####查看文件大小
    du -h file
####查看目录有多少个文件
    ls |wc -l
####查找大文件或者目录(前十)
    du -s * | sort -nr | head
####vim替换
    :%s/abc/123/g
####vim二进制文件编辑
    vim -b file
    :%!xxd
####查找文本里内容, -s屏蔽没有找到grep
    find . |xargs grep 'sda' -s
    grep -rl 123 .
####查找并删除某个后缀文件
    find . -iname '*.torrent' |xargs rm
    ls|xargs rm
####删除重复文件
    find -name '*.sh' -exec md5sum {} \;| sort | uniq -d -w 33
####替换文本, 批量替换
    sed 's/Line/line/g' file.txt # 加-i才会修改文件
    sed 's/12/abc/s' `grep 12 -rl /dir` # -i就地修改
<<<<<<< HEAD
####读取某行
    sed -n '6p' file.txt # 读取第六行
    sed '3d' file.txt # 删除第三行
    sed '$d' file.txt # 删除最后一行
=======
####kill kilall pkill
    ps aux |grep uwsgi
    kill pid
    kill -9 pi # 删除僵尸进程
    killall uwsgi # 直接删进程名
    pkill uwsgi # 同, 删单个进程用kill
    pgrep -l uwsgi # 获得详细进程pid
    xkill # 杀死桌面程序
####开机启动
    sudo vi /etc/rc.loacl >> /etc/init.d/ssh start
####断点, 限速下载
    wget -c --limit-rate=300k url
>>>>>>> 1774ead207743ee25e61b5333a28dd1836b07c27
