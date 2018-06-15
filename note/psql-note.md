## psql note

##### 登录账号

```
psql -U postgres -d postgres -p 5432 -u指定用户,-d指定数据库,-p指定端口
```

##### 增删改查

1. \l 列出所有数据库,show databases;

2. \c 连接到指定数据库,use yfuser;

3. \dt 列出所有数据表,show tables;

4. \d yfuser 查询数据结构,show create table yfuser;

5. \du 列出所有用户

6. \conninfo 列出连接数据库及用户

8. CREATE DATABASE rg_spider OWNER postgres; 创建数据库

9. drop database yfuser; 删除数据库

10. psql -U yfuser -d yfuser -h 127.0.0.1 -p 5432 登陆数据库

11. pg_dump -U yfuser -f data.sql 导出数据

12. psql -d yfuser -U yfuser -f data.sql 导入数据,需新建好数据库

13. \password 设置当前登录用户的密码

##### 数组类型操作(array)

1. 插入数组

   ```
    INSERT INTO test(id, uid) values(3, '{1, 2, 3}');
    INSERT INTO test(id, uid) values(3, array[20, 30]::int8[]);
   ```

2. 修改数组

   ```
   UPDATE test SET uid = uid || '{"test"}';    后面追加一个数组
   UPDATE test SET uid = '{"test"}' || uid;   在前面插入一个数组
   UPDATE arr_test SET uid=array_append(uid, '1'::int);   指明类型追加一个数
   UPDATE arr_test SET uid=array_append(uid, 1);   按默认int类型追加一个数
   UPDATE arr_test SET uid=array_prepend('1'::int, uid);     在前面插入一个数
   ```

3. 删除数组中的数据

   ```
   UPDATE arr_test actor=array_remove(actor, 'test'); # 删除test字符串
   ```

4. 查询数据

   ```
   SELECT * from test WHERE '金元海'=any(actor);    #actor数组中存在金元海的row
   WHERE actor@>'{"金元海","郑涵妃"}';   actor 数组中同时包含[1, 2]的
   WHERE uid<@'{1, 2}';   uid 数组被[1, 2]包含的
   SELECT * from arr_test WHERE 2=uid[1]; 使用uid 数组下标查询，下标是从1开始的
   SELECT id, uid[2] FROM arr_test; 使用下标显示
   ```

##### 词典类型操作(json)

```
from psycopg2.extras import Json # 导入json支持,否则报错
```

1. 插入json

   ```
   INSERT INTO public.zhihupage(topic_id, title, actor, data)
   VALUES (333, 'test', '{"test", "test2"}', '{"id":1,"name":"小明", "age":18}');
   ```

2. 修改json

   ```
   SET data = data::jsonb - 'name' || '{"name":"信号"}'::jsonb
   where (data->>'name') = '信号 시그널' # 删除age键值,连接后面jsonb,设置name值
   data = data::jsonb - 'test'|| '{"age": 99,"name": "hi"}'::jsonb # 删除test键值,并设置name和age键值,不存在键值插入
   ```


3. 删除json

   ```
   SET data = data::jsonb - 'age' # 删除age键值
   ```

4. 查询json

   ```
   WHERE (data->>'name') = '信号 시그널'
   ```
