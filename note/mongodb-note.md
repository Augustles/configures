
# mongodb manual

# 高并发时可以采用mongodb自带原子操作,
# 1.使用findAndModify查询并修改数据,返回之前的记录
db.book.findAndModify({
     query:{ id: bookid, status: 'free'},
     update:{
         $set:{
             status: 'busy'
         }
     }
 })
# 2. User.update({id : user_id }, param , { upsert : true })
# 3. $isolated
db.foo.update(
         { status : "A" , $isolated : 1 },
         { $inc : { count : 1 } },
         { multi: true }
     )
# 二段提交
# mongodb主从部署
###简单的主从配置
1. 从节点直接从主节点同步数据,从节点之间不相互同步
2. 从节点不可以写入, 可读
3. 容错性低
mongod --dbpath ./db/master --port 10000 --master
mongod --dbpath ./db/slave --port 10001 --slave --source 127.0.0.1:10000
####replica Set(副本集,主从集群)(读写分离)
mongod --dbpath ./db/node1 --port 10001 --replSet node
mongod --dbpath ./db/node2 --port 10002 --replSet node
mongod --dbpath ./db/node3 --port 10003 --replSet node
config ={_id:"node",members:[{_id:1,host:"127.0.0.1:10001"}]}
rs.initiate(config)
rs.add('127.0.0.1:10002')
rs.addArb('127.0.0.1:10003') # 添加仲裁节点,不存储数据,主节点挂了,secondary会成为主节点
rs.slaveOk()
####

# mongodb 3 验证
# 配置 security: authorization: enabled
# 添加role, 再添加用户,实现任意数据库读取写入权限
db.createRole({role:'sysadmin',roles:[],
privileges:[
{resource:{anyResource:true},actions:['anyAction']}
]})
db.createUser({
user:'august',
pwd:'nana',
roles:[
{role:'sysadmin',db:'admin'}
]})
# dbinfo = 'mongodb://admin:nana@192.168.1.102/nbbs?authMechanism=SCRAM-SHA-1'
db = MongoClient(dbinfo).nbbs.nzol

####from bson.objectid import ObjectId; ObjectId(s)
####show dbs; 显示所有数据库 =>show databases =>.databases
####db; 显示当前数据库对象或集合 =>show tables =>.tables
####use local; 连接一个数据库 =>use mysql =>
####show collections; 显示所有集合
####db.rpdb.find().limit(1); 显示一个文档
####db.rpdb.find(); 查找所有是一个类生成器(游标)
####db.rpdb.find_one(); 查找第一个
####$gt > $gte >= $lt < $lte <= $ne != ;模糊查找
####$in 在某个list内 $nin不在 $eq ==
####$or db.op_test.find({"$or" : [{"name":"steven"},{"age":20}]})
####$and db.op_test.find({"$and" : [{"name":"steven"},{"age":20}]})
####$not db.op_test.find({"age":{"$not":{"$lt":20}}})
####$exists 存在某个属性
####db.rpdb.find.count(); 计算文档条数

####vi /etc/mongodb.conf 加上auth=true =>添加验证
####修改blind_ip 0.0.0.0 =>外网访问
####use admin; db.addUser('admin', '123456') =>添加密码
####use admin; db.shutdownServer() =>关闭mongod
####mongod --config /etc/mongodb.conf =>启动mongod
####use DATABASE_NAME =>新建数据库
####db.dropDatabase() =>删除数据库
####db.createCollection('stats', options) =>创建集合
####db.col.drop() =>删除集合
####db.col.insert() =>插入新记录
####db.col.remove() =>删除记录
####db.col.remove({}) =>删除所有collection
####db.all.ensureIndex({'postuser'}) =>添加单索引
####db.all.ensureIndex({"topicurl" : 1, "postfloor" : 1}) =>添加组合索引
####db.user.ensureIndex({"tpid":1},{"unique":true}); =>添加唯一索引
####db.nzol.ensureIndex({'download_uri': 1, 'uri_doc_index': -1}, {unique: true, dropDups: true}) =>添加组合索引, 唯一, 去除重复项
####db.system.indexes.find() =>查看索引
####db.nzol.dropIndexes() =>删除除_id的所有索引
####all.update({'_id': tid}, {'$rename': {"postmain": "content"}}) =>修改字段名
####db.all.update({},{$unset:{"posttime":""}},{multi:true}) =>删除字段pymono暂时没有成功
####导出csv
mongoexport -h 127.0.0.1 -d amazon -c movie -f link,title,rating --csv -o test_2.csv
####mongodump 备份
  mongodump -h 127.0.0.1 -d zolbbs -c all -o /root/mongobackup/
####mongorestore 还原
  mongorestore -d newzolbb -c newall /root/mongobackup/zolbbs/all.bson
####去重
  db.alist.aggregate(
            [
                  {
                        $group:{
                              _id: {url: "$url", uri_doc_indexs: "$uri_doc_indexs"},
                              name: {$push: "$url"},
                              uri_doc_indexs: {$push: "$uri_doc_indexs"},
                              out: {$push: "$out"}
                        }
                  }
            ]
        ). forEach(function(x){
            db.temp.insert(
                  {
                    url: x.url,
                    uri_doc_indexs : x.uri_doc_indexs,
                    out: x.out,
                  }
            );
        });

