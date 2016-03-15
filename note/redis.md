##redis
sudo apt-get install redis-server
#####进入交互模式
redis-cli
set a '2333'
get a
append a 'hi'
####哈希
hmset user:1 username august password 123456
hgetall user:1 =>取哈希
####列表
lpush t redis
lpush t mysql
lpush t mongo
lrange t 0 10 =>取列表
####集合
sadd col redis
sadd col mongo
sadd col mysql
smembers ty =>取集合
