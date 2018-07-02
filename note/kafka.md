### Kafka

##### kafka是一个分布式消息队列

- **Producer/Consumer**：消息的生成者和使用者。


- **Broker**：kafka server充当broker角色，起到消息队列的作用。

- **topic/partion**：topic是一类消息的名称，一个topic下的消息可以分成多区(partion)存储，一个分区是一个有序队列(消息按接收时间依次追加，利用offset做为唯一id)，分区间消息无序。

- **zookeeper**：broker和consumer向zk注册，实现元数据的保存和交换、集群管理。

- **push/pull**：producer通过一个初始broker.list与broker建立连接，获取所有broker信息，主动向一个topic的分区leader推送信息；consumer通过zk获取broker列表，主动从broker拉取信息。

- **consumer group**：为了提高consumer处理并行性，多个consumer可以组成一个group，一个topic下的消息会保证每个group中的一个consumer消费，一个group中的consumer交错消费整个topic。简单说，topic下的一条消息会给所有的group，但一个group中只有一个consumer接收到该消息。

##### kafka安装

```
brew install kafka
```

##### 开机启动/关闭kafka,zookeeper

```
brew services start zookeeper
brew services start kafka

brew services stop kafka
brew services stop zookeeper
```

##### 直接启动

```
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties
```

##### 创建topic test

```
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

##### 查看创建的topics

```
kafka-topics --list --zookeeper localhost:2181
```

##### 在topic test控制台发送消息(生产者)

```
kafka-console-producer --broker-list localhost:9092 --topic test
```

##### 接受topic test消息(消费者)

```
kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning
```

##### 安装python客户端

```
pip install kafka-python
```

##### 生产者发送消息

```
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
t = {'test': 11, 'test2': 22}
producer.send('test', json.dumps(t).encode('utf8')) # 转换成bytes才能发送
```

##### 消费者接收消息

```

from kafka import KafkaConsumer
consumer = KafkaConsumer('test')
for msg in consumer:
    print(msg)
```

