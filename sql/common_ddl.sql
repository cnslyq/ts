drop table if exists area;
create table area(
	`id` int(6) primary key not null,
	`parent_id` bigint(20),
	`name` varchar(128),
	`level` int(1),
	`path` varchar(64)
) ENGINE=InnoDB;
alter table area add index area_name_idx (`name`);

drop table if exists dict;
create table dict(
	`id` bigint(20) primary key not null auto_increment,
	`type` varchar(16),
	`name` varchar(16),
	`value` int(8)
) ENGINE=InnoDB;

