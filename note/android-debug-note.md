## 安卓调试
adb install 1.apk 安装apk安装包
adb uninstall 1.apk 卸载安装包
adb shell dumpsys activity | grep mFocusedActivity 显示当前应用activity
adb shell ps |grep bobo 查看当前bobo pid
adb forward tcp:8800 jdwp:30203 端口转发以便smali,ida调用
adb logcat -s lil 显示filter为lil日志

#### apktool
apktool d 1.apk 反编译,实际上baksmali工具封装
tar -cvf 1.tar 1 打包文件夹

#### jadx
解析dex文件=》smali源码=》解析smali指令=》借助asm生成class文件=》解析class文件得到Java源码


