drop table url.myurls;
drop table url.category;
drop table url.uricat;
-- create tables
create table url.myurls(uid int unique not null,uri varchar(255),desc varchar(255));
create table url.category(cid int unique not null, catname varchar(60), desc varchar(255));
create table url.uricat(uid int, cid int);
