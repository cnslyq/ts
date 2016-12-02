drop table if exists stock_info;
create table stock_info(
	`id` bigint(20) primary key not null auto_increment,
	`code` varchar(8),
	`name` varchar(16),
	`industry` int(8),
	`concept` varchar(256),
	`area` int(6),
	`is_sme` int(1),
	`is_gem` int(1),
	`is_risk` int(1),
	`is_hs300` int(1),
	`is_sz50` int(1),
	`is_zz500` int(1),
	`is_stop` int(1),
	`is_pause` int(1),
	`hs300_date` date,
	`hs300_weight` double,
	`list_date` date,
	`stop_date` date,
	`pause_date` date,
	`create_date` timestamp not null default CURRENT_TIMESTAMP,
	`update_date` timestamp
) ENGINE=InnoDB;
alter table stock_info add index stock_info_code_idx (`code`);

