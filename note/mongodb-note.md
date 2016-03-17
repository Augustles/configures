
# mongodb manual

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

####use DATABASE_NAME =>新建数据库
####db.dropDatabase() =>删除数据库
####db.createCollection('stats', options) =>创建集合
####db.col.insert() =>插入新记录
####db.col.remove() =>删除记录
####db.col.remove({}) =>删除所有collection
####db.all.ensureIndex({'postuser'}) =>添加单索引
####db.all.ensureIndex({"topicurl" : 1, "postfloor" : 1}) =>添加组合索引
####db.user.ensureIndex({"tpid":1},{"unique":true}); =>添加唯一索引
####db.Metadata.CreateIndex(new Document { { "UserId", 1 }, { "UserName", -1 } }, false);
####db.system.indexes.find() =>查看索引
####导出csv
mongoexport -h 127.0.0.1 -d amazon -c movie -f link,title,rating --csv -o test_2.csv
####mongodump 备份
  mongodump -h 127.0.0.1 -d zolbbs -c all -o /root/mongobackup/
####mongorestore 还原
  mongorestore -d newzolbb -c newall /root/mongobackup/zolbbs/all.bson
