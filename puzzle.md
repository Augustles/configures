##记录puzzle

1. scapy捕捉到的Raw load具体是什么, http协议中requests如何发送 (一般有session来访问一个需登录网站,s.post(url,data,headers))
2. yield可以让程序暂停, 让函数有多个出口入口, 但是该如何控制接收和发送send
3. gevent.sleep()可以让协程回到主loop调度中, 在什么时候切换回协程???
gevent有一个主hub greenlet,会先回到主hub greenlet然后再switc相应的greenlet
4. phantomjs 如何发送cookie, 报错:
WebDriverException: Message: {"errorMessage":"Can only set Cookies for the current domain"}
5. phantomjs 如何发送data(body)
