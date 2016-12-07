drop table if exists invest_forecast;
create table invest_forecast(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`type` varchar(8),
	`report_date` date,
	`pre_eps` double,
	`range` varchar(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table invest_forecast add index invest_forecast_date_idx (`year`, `quarter`);
alter table invest_forecast add index invest_forecast_code_idx (`code`);

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
	`range` varchar(16),
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
	`name` varchar(16),
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
alter table invest_new_stock add index invest_new_stock_date_idx (`date`);
alter table invest_new_stock add index invest_new_stock_code_idx (`code`);

drop table if exists invest_margin_sh_smry;
create table invest_margin_sh_smry(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`rzye` int(16),
	`rzmre` int(16),
	`rqyl` int(16),
	`rqylje` int(16),
	`rqmcl` int(16),
	`rzrqjyzl` int(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sh_smry add index invest_margin_sh_smry_date_idx (`opDate`);

drop table if exists invest_margin_sh_dtl;
create table invest_margin_sh_dtl(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`stockCode` varchar(8),
	`securityAbbr` varchar(16),
	`rzye` int(16),
	`rzmre` int(16),
	`rzche` int(16),
	`rqyl` int(16),
	`rqmcl` int(16),
	`rqchl` int(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sh_dtl add index invest_margin_sh_dtl_date_idx (`opDate`);
alter table invest_margin_sh_dtl add index invest_margin_sh_dtl_code_idx (`stockCode`);

drop table if exists invest_margin_sz_smry;
create table invest_margin_sz_smry(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`rzye` int(16),
	`rzmre` int(16),
	`rqyl` int(16),
	`rqmcl` int(16),
	`rqye` int(16),
	`rzrqye` int(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sz_smry add index invest_margin_sz_smry_date_idx (`opDate`);

drop table if exists invest_margin_sz_dtl;
create table invest_margin_sz_dtl(
	`id` bigint(20) primary key not null auto_increment,
	`opDate` date,
	`stockCode` varchar(8),
	`securityAbbr` varchar(16),
	`rzmre` int(16),
	`rzye` int(16),
	`rqmcl` int(16),
	`rqyl` int(16),
	`rqye` int(16),
	`rzrqye` int(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table invest_margin_sz_dtl add index invest_margin_sz_dtl_date_idx (`opDate`);
alter table invest_margin_sz_dtl add index invest_margin_sz_dtl_code_idx (`stockCode`);
