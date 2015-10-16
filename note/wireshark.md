## wireshark python scapy bettercap

Capture -> interfaces 选择你的网卡 -> 抓包
Ctrl + M 给数据包做标记
Shift + Ctrl + B/N 数据包前后切换的快捷按键

View -> Coloring Rules 协议包的颜色调整

Filter -> 这里可以暂时写上你要过滤数据包
例如：ip.addr==IP地址
常见的比较操作符
== 等于
!= 不等于
> 大于
< 小于
>= 大于等于
<= 小于等于

Statistics -> Endpoints 查看端点
Statistics -> Conversations 查看网络会话
Statistics -> Packet lenghts 查看数据包长度
Statistics -> IO Graphs 查看IO图
Statistics -> Flow Graph 查看数据流图

Ethernet II -> Destination 数据包目的地
Ethernet II -> Source MAC地址

IPV4
Internat Protocol -> Version (IP版本号)
Internat Protocol -> Header length (头长度)
Internat Protocol -> Total length (首部和载荷长度)
Internat Protocol -> Time to live (TTL区域数值)
Internat Protocol -> Source (请求源地址)
Internat Protocol -> Destination （请求目标地址）

TCP
Transmission Control Protocol -> Source Port 源端口
Transmission Control Protocol -> Destination Port 目的端口
Transmission Control Protocol -> Sequence number 序号
Transmission Control Protocol -> Acknowledgment number 确认号
Transmission Control Protocol -> Flags (用来标记TCP数据包类型)
URG、ACK、FIN、SYN、RST、PSH ..
Transmission Control Protocol -> Window size value 缓冲字节大小
Transmission Control Protocol -> checksum 校验和
这个就是跟TCP数据完整性相关
Urgent Pointer 紧急指针

数据包右键 Follow tcp 选项 可以看到数据包内更详细的内容

Ctrl + F -> String -> Packet Bytes 查找先关字符

POP3暴力破解
+OK User successfully logged on.   //认证成功

SMTP暴力破解
235 2.7.0 Authentication successful.    //认证成功

漏洞挖掘简单的思路，例如：APP








