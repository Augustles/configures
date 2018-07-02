--postgres创建数据库及表结构
create database rg_spider; --创建filminfo数据库
\c rg_spider;

CREATE TABLE filminfo
(
    doubanid integer,
    fid SERIAL, --自增id会生成一个SEQUENCE
    title character varying,
    actor character varying[], --存储为arrary
    data jsonb, --存储为json
    "desc" text,
    PRIMARY KEY (doubanid)
);
comment on table filminfo is '豆瓣爬虫表';
comment on column filminfo.desc is 'desc 为postgres的keyword需要分号包容'; --字段注释用单引号
comment on column filminfo.doubanid is '豆瓣ID';
create unique index filminfo_doubanid on filminfo(doubanid); --创建唯一索引
ALTER SEQUENCE filminfo_fid_seq RESTART WITH 100000; --fid自增id从10000开始
SELECT setval('filminfo_fid_seq', max(fid)) FROM filminfo; --把表中fid最大的那个值，付值给计数器
ALTER TABLE filminfo ALTER COLUMN fid SET DEFAULT nextval('filminfo_fid_seq'); --设置fid的值，从计数器获取

CREATE TABLE filminfo_alias
(
	alias character varying[]
) INHERITS(filminfo);
comment on table filminfo_alias is '豆瓣alias表,表继承测试';
comment on column filminfo_alias.alias is '别名';
create unique index filminfo_alias_doubanid on filminfo_alias(doubanid); --创建唯一索引


-- create table filminfo_test (like filminfo_alias including all); --继承所有的,不包括数据,但是数据不同步
-- 表继承测试

CREATE TABLE IF NOT EXISTS cities
(   --父表
    name        text,
    population float,
    altitude     int
);
CREATE TABLE IF NOT EXISTS capitals
( --子表
    state      char(2)
) INHERITS (cities);
INSERT INTO cities values('Las Vegas', 1.53, 2174);  --插入父表
INSERT INTO cities values('Mariposa',3.30,1953);     --插入父表
INSERT INTO capitals values('Madison',4.34,845,'WI');--插入子表,插入子表数据,会同步出现在父表,数据同步,删除子表数据,父表数据删除,删除父表数据,子表也会删除
SELECT name, altitude FROM cities WHERE altitude > 500; --父表和子表的数据均被取出。
SELECT p.relname, c.name, c.altitude FROM cities c,pg_class p WHERE c.altitude > 500 and c.tableoid = p.oid; --查看所属表
