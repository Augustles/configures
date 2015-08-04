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