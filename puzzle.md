##记录puzzle

1. scapy捕捉到的Raw load具体是什么, http协议中requests如何发送 (一般有session来访问一个需登录网站,s.post(url,data,headers))
Raw load里的数据是一些字节码
2. yield可以让程序暂停, 让函数有多个出口入口, 但是该如何控制接收和发送send
要在单线程实现异步, 一般有两种方法, 用yield挂起函数, 还有就是采用类似线程池的方法
在tornado 的gen中, 遇到耗时对象时候, 可以yield挂起函数, 相当于在执行一个函数
然后用raise gen.Return来返回对象,相当于return
3. gevent.sleep()可以让协程回到主loop调度中, 在什么时候切换回协程???
gevent有一个主hub greenlet,会先回到主hub
其中有一个Waiter对象,他是各个greenlet的信使,通过设置Waiter的greenlet属性
greenlet再switch相应的greenlet
4. phantomjs 如何发送cookie, 报错:
WebDriverException: Message: {"errorMessage":"Can only set Cookies for the current domain"}
5. phantomjs 如何发送data(body)
