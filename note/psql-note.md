##psql note

####增删改查
1. \l 列出所有数据库,show databases;
2. \c 连接到指定数据库,use yfuser;
3. \dt 列出所有数据表,show tables;
4. \d yfuser 查询数据结构,show create table yfuser;
5. \du 列出所有用户
6. \conninfo 列出连接数据库及用户
7. create database yfuser; 创建数据库
8. drop database yfuser; 删除数据库
9. psql -U yfuser -d yfuser -h 127.0.0.1 -p 5432 登陆数据库
10. pg_dump -U yfuser -f data.sql 导出数据
11. psql -d yfuser -U yfuser -f data.sql 导入数据,需新建好数据库
