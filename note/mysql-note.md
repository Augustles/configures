##mysql note

###pip install sqlalchemy
* https://www.keakon.net/2012/12/03/SQLAlchemy%E4%BD%BF%E7%94%A8%E7%BB%8F%E9%AA%8C
#### show databases; 查询存在数据库
#### create database august; 创建数据库, CREATE DATABASE august DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
#### drop database august; 删除数据库
#### use august; 切换数据库
#### show tables; 查看数据库中存在的表
#### create table user (name varchar(20),password varchar(20));  创建user表
#### drop table user; 删除user表
#### delete from douban; 删除douban表里内容
#### desc user; 查看user表结构
#### select * from user; 查询user表所有内容
#### insert into user (name,password) values('lily','czxklla'); values值为字符串,否则会报错 插入user表数据
#### insert ignore into () values(); 如果存在不插入(表中需存在主索引)
#### select * from user where binary name='lily'; 查询user表中name是lily,binary参数区分大小写
#### update user set password='321' where name='lily'; 更新user表中lily的password数据
#### delete from user where name='lily'; 删除user表中lily的数据
#### select * from user where name like '%tom'; 模糊查询user表中存在name是tom
#### select * from user order by name asc; 对user表中name进行倒序排列
#### select * from user order by name asc limit 5; 限制查询条数
#### alter table user rename user_t;  修改user表名
#### alter table user_t drop password;  删除password字段
#### alter table tablename change old_field_name new_field_name old_type; 修改字段名
#### alter table user_t add password varchar(20) first;  添加password字段至first
#### alter table user_t modify password char(20);  修改password字段属性
#### alter table user_t_t alter password set default '123456';  修改字段默认值,默认值注意字符串
#### alter talbe user_t_t type =myisam;  修改user_t_t表类型为myisam???
#### alter table user_t add primary key(password);  添加主键, 主键是一个特殊的索引, primary key不可重复
#### alter table user_t drop primary key;  删除主键
#### alter table user_t add index index_name(name);  添加索引,索引可以大大加快MySQL的检索速度
#### alter table user_t drop index name;  删除索引
#### alter table user add nuique index(download_uri,uri_doc_index); 添加组合唯一索引
#### show index from user_t;  查看索引,主键
#### show create table user_t;  显示完整的user_t表结构

#### select * from test_a left  join test_b on test_a.name=test_b.name;  left join查询,左侧表里的信息全部查询出来,右边以NULL代替
#### select * from test_b right join test_b on test_a.name=test_b.name;  right join, 右侧表里的信息全部查询出来,左边以NULL代替
#### select * from test_a inner join test_b on test_a.name=test_b.name;  inner join,左右两边都相等才会查询显示


#### 查询数据库的容量
#### SELECT table_schema AS 'Db Name',Round( Sum( data_length + index_length ) / 1024 / 1024, 3 ) AS 'Db Size (MB)',
#### Round( Sum( data_free ) / 1024 / 1024, 3 ) AS 'Free Space (MB)' FROM information_schema.tables GROUP BY table_schema ;

#### select * from douban into outfile '/tmp/out.csv' fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 导出csv文件

#### select count(*) from amazon; 计算记录条数
#### select * from amazon limit 5;


#### select version(); mysql版本信息
#### select database(); 当前数据库名
#### select user(); 当前用户名
#### show status; 服务器状态
#### show variables; 服务器配置变量
#### 主键(primary key),主键也是一个特殊的索引
#### 外键(foreign key),外键用来建立或者和加强两个表数据之间的链接的一列或者多列
#### 外键约束主要用来维护两个表之间数据的一致性
#### 主键一定是唯一性索引,但唯一性索引不一定为主键
#### 一个表中只能有一个主键,可以有多个唯一性索引
#### 存储引擎,MyISAM查询较多使用,InnoDB写入较多使用
#### 主键列不允许空值,唯一性索引允许空值
#### 主键能被其他字段作外键引用,索引不能作为外键引用
#### [http://www.w3cschool.cc/mysql/mysql-alter.html]
#### [http://www.cnblogs.com/aspnethot/articles/1397130.html]

####mysql修改密码
use mysql
update user set password=password('123456') where user='root' and host='localhost';
flush privileges;

####执行外部sql语句, 
mysql -uroot -p123456 < yingshi.sql

####mysql存储引擎myisam和innodb的区别
innodb支持事务,myisam不支持
innodb支持行级锁,myisam不支持
innodb支持mvcc,myisam不支持
innodb支持外键,myisam不支持
innodb不支持全文搜索,myisam支持

####innodb引擎4大特性
插入缓存(insert buffer)
二次写(double write)
自适应哈希索引(ahi)
预读(read ahead)

####myisam&innodb select count()哪个更快
myisam更快,因为myisam内部维护了一个计数器,可以直接调用

####drop,delete,truncate区别
drop直接删除表, 删除表结构及索引
truncate删除表中的数据,再插入时自增长id从1开始,
delete可以加where子句,保留增长id,会一行一行删除

####视图的作用，视图可以更改么？
视图是虚拟的表
视图包含动态检索数据的查询,不包含任何列或数据
视图不能被索引,也不能有关联的触发器和默认值
视图可以用来简化检索,保护数据

####sql语句优化
尽量避免在where子句中使用!=或者<>操作符,否则mysql会放弃索引进行全表扫描
尽量避免在where子句中对字段进行null值判断,可以设置默认值为0或者空字符串
where num=0 or name=''
可以用exists代替in

CREATE TABLE `douban` (
  `linkmd5id` char(32) NOT NULL COMMENT 'url md5编码id',
  `title` text COMMENT '标题',
  `description` text COMMENT '描述',
  `link` text  COMMENT 'url链接',
  `created` datetime DEFAULT NULL  COMMENT '创建时间',
  `updated` datetime DEFAULT NULL  COMMENT '最后更新时间',
  PRIMARY KEY (`linkmd5id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


python manage.py schemamigration youappname --initial

# --initial在数据库创建models定义的表，以及South需要的south_migrationhistory表，另外会在youappname目录下面创建一个migrations的子目录
#以后每次对models更改后，可以运行以下两条命令同步到数据库
python manage.py schemamigration youappname --auto     #检测对models的更改

python manage.py migrate youappnam  #将更改反应到数据库
