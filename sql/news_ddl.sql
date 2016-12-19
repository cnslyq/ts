drop table if exists news_real;
create table news_real(
	`id` bigint(20) primary key not null auto_increment,
	`classify` varchar(16),
	`title` varchar(128),
	`time` varchar(16),
	`url` varchar(128),
	`content` mediumtext,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;

drop table if exists news_notices;
create table news_notices(
	`id` bigint(20) primary key not null auto_increment,
	`code` varchar(8),
	`date` date,
	`title` varchar(128),
	`type` varchar(32),
	`url` varchar(128),
	`content` mediumtext,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table news_notices add index news_notices_code_idx (`code`);
alter table news_notices add index news_notices_date_idx (`date`);
