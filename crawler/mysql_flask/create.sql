create user test identified by '654321';

create database bilibili;

grant all privileges on bilibili.* to test;

use bilibili;
create table `myrank12`
(
  `title` varchar(500) not null,
  `author` varchar(500) not null,
  `aid`    varchar(50)    not null,
  `bvid`   varchar(50)  not null,
  `coins`  int    not null,
  `play`   int    not null,
  `video_review` int    not null,
  `ranking` int   not null,
  `date`   varchar(50) not null,
  PRIMARY KEY(`bvid`,`date`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
