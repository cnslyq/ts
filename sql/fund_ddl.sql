drop table if exists fund_nav_open;
create table fund_nav_open(
	`id` bigint(20) primary key not null auto_increment,
	`nav_date` date,
	`symbol` varchar(8),
	`sname` varchar(32),
	`per_nav` double,
	`total_nav` double,
	`yesterday_nav` double,
	`nav_a` double,
	`nav_rate` double,
	`fund_manager` varchar(32),
	`jjlx` varchar(32),
	`jjzfe` bigint(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table fund_nav_open add index fund_nav_open_code_idx (`symbol`);
alter table fund_nav_open add index fund_nav_open_date_idx (`nav_date`);

drop table if exists fund_nav_close;
create table fund_nav_close(
	`id` bigint(20) primary key not null auto_increment,
	`nav_date` date,
	`symbol` varchar(8),
	`sname` varchar(32),
	`per_nav` double,
	`total_nav` double,
	`nav_rate` double,
	`discount_rate` double,
	`start_date` date,
	`end_date` date,
	`fund_manager` varchar(32),
	`jjlx` varchar(32),
	`jjzfe` bigint(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table fund_nav_close add index fund_nav_close_code_idx (`symbol`);
alter table fund_nav_close add index fund_nav_close_date_idx (`nav_date`);

drop table if exists fund_nav_grading;
create table fund_nav_grading(
	`id` bigint(20) primary key not null auto_increment,
	`nav_date` date,
	`symbol` varchar(8),
	`sname` varchar(32),
	`per_nav` double,
	`total_nav` double,
	`nav_rate` double,
	`discount_rate` double,
	`start_date` date,
	`end_date` date,
	`fund_manager` varchar(32),
	`jjlx` varchar(32),
	`jjzfe` bigint(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table fund_nav_grading add index fund_nav_grading_code_idx (`symbol`);
alter table fund_nav_grading add index fund_nav_grading_date_idx (`nav_date`);

drop table if exists fund_nav_history;
create table fund_nav_history(
	`id` bigint(20) primary key not null auto_increment,
	`symbol` varchar(8),
	`date` date,
	`value` double,
	`total` double,
	`change` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table fund_nav_history add index fund_nav_history_code_idx (`symbol`);
alter table fund_nav_history add index fund_nav_history_date_idx (`date`);

drop table if exists fund_info;
create table fund_info(
	`id` bigint(20) primary key not null auto_increment,
	`symbol` varchar(8),
	`jjqc` varchar(32),
	`jjjc` varchar(16),
	`clrq` date,
	`ssrq` date,
	`xcr` varchar(32),
	`ssdd` varchar(32),
	`Type1Name` varchar(16),
	`Type2Name` varchar(16),
	`Type3Name` varchar(16),
	`jjgm` double,
	`jjfe` double,
	`jjltfe` double,
	`jjferq` date,
	`quarter` int(1),
	`glr` varchar(32),
	`tgr` varchar(32),
	`create_date` timestamp not null default CURRENT_TIMESTAMP,
	`update_date` timestamp
) ENGINE=InnoDB;
alter table fund_info add index fund_info_code_idx (`symbol`);
