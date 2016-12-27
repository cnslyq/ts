drop table if exists invest_profit;
create table invest_profit(
	`id` bigint(20) primary key not null auto_increment,
	`code` varchar(8),
	`name` varchar(16),
	`year` int(4),
	`report_date` date,
	`divi` double,
	`shares` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table invest_profit add index invest_profit_code_idx (`code`);

drop table if exists invest_forecast_history;
create table invest_forecast_history(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`type` varchar(8),
	`report_date` date,
	`pre_eps` double,
	`range` varchar(32),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table invest_forecast_history add index invest_forecast_history_date_idx (`year`, `quarter`);
alter table invest_forecast_history add index invest_forecast_history_code_idx (`code`);

drop table if exists invest_lifted;
create table invest_lifted(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`count` double,
	`ratio` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table invest_lifted add index invest_lifted_date_idx (`date`);
alter table invest_lifted add index invest_lifted_code_idx (`code`);

drop table if exists invest_fund_hold;
create table invest_fund_hold(
	`id` bigint(20) primary key not null auto_increment,
	`code` varchar(8),
	`name` varchar(32),
	`date` date,
	`nums` int(4),
	`nlast` int(4),
	`count` double,
	`clast` double,
	`amount` double,
	`ratio` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table invest_fund_hold add index invest_fund_hold_date_idx (`date`);
alter table invest_fund_hold add index invest_fund_hold_code_idx (`code`);

drop table if exists invest_new_stock;
create table invest_new_stock(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`code` varchar(8),
	`xcode` varchar(8),
	`name` varchar(16),
	`ipo_date` date,
	`issue_date` date,
	`amount` double,
	`markets` double,
	`price` double,
	`pe` double,
	`limit` double,
	`funds` double,
	`ballot` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_new_stock add index invest_new_stock_date_idx (`ipo_date`);
alter table invest_new_stock add index invest_new_stock_code_idx (`code`);

drop table if exists invest_margin_sh_smry;
create table invest_margin_sh_smry(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`rzye` bigint(16),
	`rzmre` bigint(16),
	`rqyl` bigint(16),
	`rqylje` bigint(16),
	`rqmcl` bigint(16),
	`rzrqjyzl` bigint(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sh_smry add index invest_margin_sh_smry_date_idx (`opDate`);

drop table if exists invest_margin_sh_dtl;
create table invest_margin_sh_dtl(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`stockCode` varchar(8),
	`securityAbbr` varchar(16),
	`rzye` bigint(16),
	`rzmre` bigint(16),
	`rzche` bigint(16),
	`rqyl` bigint(16),
	`rqmcl` bigint(16),
	`rqchl` bigint(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sh_dtl add index invest_margin_sh_dtl_date_idx (`opDate`);
alter table invest_margin_sh_dtl add index invest_margin_sh_dtl_code_idx (`stockCode`);

drop table if exists invest_margin_sz_smry;
create table invest_margin_sz_smry(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`rzye` bigint(16),
	`rzmre` bigint(16),
	`rqyl` bigint(16),
	`rqmcl` bigint(16),
	`rqye` bigint(16),
	`rzrqye` bigint(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sz_smry add index invest_margin_sz_smry_date_idx (`opDate`);

drop table if exists invest_margin_sz_dtl;
create table invest_margin_sz_dtl(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`stockCode` varchar(8),
	`securityAbbr` varchar(16),
	`rzmre` bigint(16),
	`rzye` bigint(16),
	`rqmcl` bigint(16),
	`rqyl` bigint(16),
	`rqye` bigint(16),
	`rzrqye` bigint(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sz_dtl add index invest_margin_sz_dtl_date_idx (`opDate`);
alter table invest_margin_sz_dtl add index invest_margin_sz_dtl_code_idx (`stockCode`);

drop table if exists invest_top10_holders; 
create table invest_top10_holders(
	`id` bigint(20) primary key not null auto_increment,
	`code` varchar(8),
	`quarter` date,
	`name` varchar(128),
	`hold` double,
	`h_pro` double,
	`sharetype` varchar(64),
	`status` varchar(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table invest_top10_holders add index invest_top10_holders_date_idx (`quarter`);
alter table invest_top10_holders add index invest_top10_holders_code_idx (`code`);