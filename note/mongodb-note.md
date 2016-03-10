
# mongodb manual

####show dbs; 显示所有数据库 =>show databases =>.databases
####db; 显示当前数据库对象或集合 =>show tables =>.tables
####use local; 连接一个数据库 =>use mysql =>
####show collections; 显示所有集合
####db.rpdb.find().limit(1); 显示一个文档
####db.rpdb.find.count(); 计算文档条数

####use DATABASE_NAME =>新建数据库
####db.dropDatabase() =>删除数据库
####db.col.insert() =>插入新记录
####db.col.remove() =>删除记录
####db.col.remove({}) =>删除所有collection
####db.user.ensureIndex({"tpid":1},{"unique":true}); =>添加唯一索引
####db.system.indexes.find() =>查看索引
mongoexport -h 127.0.0.1 -d amazon -c movie -f link,title,rating --csv -o test_2.csv 
