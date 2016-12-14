drop table if exists news_real;
create table news_real(
	`id` bigint(20) primary key not null auto_increment,
	`classify` varchar(16),
	`title` varchar(128),
	`time` varchar(16),
	`url` varchar(128),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
