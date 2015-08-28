##mysql note

#### show databases; 查询存在数据库
#### create database august; 创建数据库, CREATE DATABASE august DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
#### drop database august; 删除数据库
#### use august; 切换数据库
#### show tables; 查看数据库中存在的表
#### create table user (name varchar(20),password varchar(20));  创建user表
#### desc user; 查看user表结构
#### select * from user; 查询user表所有内容
#### insert into user (name,password) values('lily','czxklla'); values值为字符串,否则会报错 插入user表数据
#### select * from user where binary name='lily'; 查询user表中name是lily,binary参数区分大小写
#### update user set password='321' where name='lily'; 更新user表中lily的password数据
#### delete from user where name='lily'; 删除user表中lily的数据
#### select * from user where name like '%tom'; 模糊查询user表中存在name是tom
#### select * from user order by name asc; 对user表中name进行倒序排列
#### select * from user order by name asc limit 5; 限制查询条数
#### alter table user rename user_t;  修改user表名
#### alter table user_t drop password;  删除password字段
#### alter table user_t add password varchar(20) first;  添加password字段至first
#### alter table user_t modify password char(20);  修改password字段属性
#### alter table user_t_t alter password set default '123456';  修改字段默认值,默认值注意字符串
#### alter talbe user_t_t type =myisam;  修改user_t_t表类型为myisam???
#### alter table user_t add primary key(password);  添加主键
#### alter table user_t drop primary key;  删除主键
#### alter table user_t add index index_name(name);  添加索引,索引可以大大加快MySQL的检索速度
#### alter table user_t drop index name;  删除索引
#### show index from user_t;  查看索引,主键
#### show create table user_t;  显示完整的user_t表结构

#### select * from test_a left  join test_b on test_a.name=test_b.name;  left join查询,左侧表里的信息全部查询出来,右边以NULL代替
#### select * from test_b right join test_b on test_a.name=test_b.name;  right join, 右侧表里的信息全部查询出来,左边以NULL代替
#### select * from test_a inner join test_b on test_a.name=test_b.name;  inner join,左右两边都相等才会查询显示


#### 查询数据库的容量
#### SELECT table_schema AS 'Db Name',Round( Sum( data_length + index_length ) / 1024 / 1024, 3 ) AS 'Db Size (MB)',
#### Round( Sum( data_free ) / 1024 / 1024, 3 ) AS 'Free Space (MB)' FROM information_schema.tables GROUP BY table_schema ;



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
#### 主键列不允许空值,唯一性索引允许空值
#### 主键能被其他字段作外键引用,索引不能作为外键引用
#### [http://www.w3cschool.cc/mysql/mysql-alter.html]
#### [http://www.cnblogs.com/aspnethot/articles/1397130.html]
